from refiners.fluxion.context import Contexts
from refiners.fluxion.layers import Chain, Conv2d, SiLU, Lambda, Passthrough, UseContext, Sum, Identity
from refiners.foundationals.latent_diffusion.unet import DownBlocks, MiddleBlock, ResidualBlock, TimestepEncoder
from refiners.adapters.range_adapter import RangeAdapter2d
from typing import cast, Iterable
from torch import Tensor, device as Device, dtype as DType


class ConditionEncoder(Chain):
    """Encode an image to be used as a condition for Controlnet.

    Input is a `batch 3 width height` tensor, output is a `batch 320 width//8 height//8` tensor.
    """

    structural_attrs = ["out_channels"]

    def __init__(self, device: Device | str | None = None, dtype: DType | None = None) -> None:
        self.out_channels = (16, 32, 96, 256)
        super().__init__(
            Chain(
                Conv2d(
                    in_channels=3,
                    out_channels=self.out_channels[0],
                    kernel_size=3,
                    stride=1,
                    padding=1,
                    device=device,
                    dtype=dtype,
                ),
                SiLU(),
            ),
            *(
                Chain(
                    Conv2d(
                        in_channels=self.out_channels[i],
                        out_channels=self.out_channels[i],
                        kernel_size=3,
                        padding=1,
                        device=device,
                        dtype=dtype,
                    ),
                    SiLU(),
                    Conv2d(
                        in_channels=self.out_channels[i],
                        out_channels=self.out_channels[i + 1],
                        kernel_size=3,
                        stride=2,
                        padding=1,
                        device=device,
                        dtype=dtype,
                    ),
                    SiLU(),
                )
                for i in range(len(self.out_channels) - 1)
            ),
            Conv2d(
                in_channels=self.out_channels[-1],
                out_channels=320,
                kernel_size=3,
                padding=1,
                device=device,
                dtype=dtype,
            ),
        )


class Controlnet(Passthrough):
    structural_attrs = ["name", "scale"]

    def __init__(self, name: str, device: Device | str | None = None, dtype: DType | None = None) -> None:
        """Controlnet is a Half-UNet that collects residuals from the UNet and uses them to condition the UNet.

        Input is a `batch 3 width height` tensor, output is a `batch 1280 width//8 height//8` tensor with residuals
        stored in the context.

        It has to use the same context as the UNet: `unet` and `sampling`.
        """
        self.name = name
        self.scale: float = 1.0
        super().__init__(
            TimestepEncoder(context_key=f"timestep_embedding_{name}", device=device, dtype=dtype),
            Lambda(lambda x: x.narrow(dim=1, start=0, length=4)),  # support inpainting
            DownBlocks(in_channels=4, device=device, dtype=dtype),
            MiddleBlock(device=device, dtype=dtype),
        )

        # We run the condition encoder at each step. Caching the result
        # is not worth it as subsequent runs take virtually no time (FG-374).
        self.DownBlocks[0].append(
            Sum(
                Identity(),
                Chain(
                    UseContext("controlnet", f"condition_{name}"),
                    ConditionEncoder(device=device, dtype=dtype),
                ),
            ),
        )
        for residual_block in self.layers(ResidualBlock):
            chain = residual_block.Chain
            range_adapter = RangeAdapter2d(
                target=chain.Conv2d_1,
                channels=residual_block.out_channels,
                embedding_dim=1280,
                context_key=f"timestep_embedding_{self.name}",
                device=device,
                dtype=dtype,
            )
            range_adapter.inject(chain)
        for n, block in enumerate(cast(Iterable[Chain], self.DownBlocks)):
            assert hasattr(block[0], "out_channels"), (
                "The first block of every subchain in DownBlocks is expected to respond to `out_channels`,"
                f" {block[0]} does not."
            )
            out_channels: int = block[0].out_channels
            block.append(
                Passthrough(
                    Conv2d(
                        in_channels=out_channels, out_channels=out_channels, kernel_size=1, device=device, dtype=dtype
                    ),
                    Lambda(self._store_nth_residual(n)),
                )
            )
        self.MiddleBlock.append(
            Passthrough(
                Conv2d(in_channels=1280, out_channels=1280, kernel_size=1, device=device, dtype=dtype),
                Lambda(self._store_nth_residual(12)),
            )
        )

    def init_context(self) -> Contexts:
        return {
            "unet": {"residuals": [0.0] * 13},
            "sampling": {"shapes": []},
            "controlnet": {f"condition_{self.name}": None},
            "range_adapter": {f"timestep_embedding_{self.name}": None},
        }

    def _store_nth_residual(self, n: int):
        def _store_residual(x: Tensor):
            residuals = self.use_context("unet")["residuals"]
            residuals[n] = residuals[n] + x * self.scale
            return x

        return _store_residual

    def set_controlnet_condition(self, condition: Tensor) -> None:
        self.set_context("controlnet", {f"condition_{self.name}": condition})

    def set_scale(self, scale: float) -> None:
        self.scale = scale
