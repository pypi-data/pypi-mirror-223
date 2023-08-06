<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/finegrain-ai/refiners/main/assets/logo_dark.png">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/finegrain-ai/refiners/main/assets/logo_light.png">
  <img alt="Finegrain Refiners Library" width="352" height="128" style="max-width: 100%;">
</picture>

**The simplest way to train and run adapters on top of foundational models**

______________________________________________________________________

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/refiners)](https://pypi.org/project/refiners/)
[![PyPI Status](https://badge.fury.io/py/refiners.svg)](https://badge.fury.io/py/refiners)
[![license](https://img.shields.io/badge/license-MIT-blue)](/LICENSE)
</div>


- [Motivation](#motivation)
- [Design](#design)
- [Downsides](#downsides)
- [Overview](#overview)
- [Key Concepts](#key-concepts)
    - [The Chain class](#the-chain-class)
    - [The Context API](#the-context-api)
    - [The Adapter API](#the-adapter-api)
- [Getting Started](#getting-started)
  - [Install](#install)
  - [Hello World](#hello-world)
- [Training](#training)
- [Credits](#credits)
- [Citation](#citation)


## Motivation

At [Finegrain](https://finegrain.ai), we're on a mission to automate product photography. Given our "no human in the loop approach", nailing the quality of the outputs we generate is paramount to our success. 

That's why we're building Refiners.

It's a framework to easily bridge the last mile quality gap of foundational models like Stable Diffusion or Segment Anything Model (SAM), by adapting them to specific tasks with lightweight trainable and composable patches.

We decided to build Refiners in the open. 

It's because model adaptation is a new paradigm that goes beyond our specific use cases. Our hope is to help people looking at creating their own adapters save time, whatever the foundation model they're using.

## Design

We are huge fans of PyTorch (we actually were core committers to [Torch](http://torch.ch/) in another life), but we felt it's too low level for the specific model adaptation task: PyTorch models are generally hard to understand, and their adaptation requires intricate ad hoc code.

Instead, we needed:

- A model structure that's human readable so that you know what models do and how they work right here, right now
- A mechanism to easily inject parameters in some target layers, or between them
- A way to easily pass data (like a conditioning input) between layers even when deeply nested
- Native support for iconic adapter types like LoRAs and their community trained incarnations (hosted on [Civitai](http://civitai.com/) and the likes)

Refiners is designed to tackle all these challenges while remaining just one abstraction away from our beloved PyTorch.

## Downsides

As they say, there is no free lunch. Given Refiners comes with a new model structure, it can only work with models implemented that way. For now, we support Stable Diffusion 1.5, but more is in the making (SDXL, SAM, ...) - stay tuned.

## Overview

The Refiners library is made of:

1. An abstraction layer (called Fluxion) on top of [PyTorch](https://pytorch.org/) to easily build models
2. A zoo of compatible foundational models
3. Adapter APIs to easily patch supported foundational models
4. Training utils to train concrete adapters
5. Conversion scripts to easily use existing community adapters

## Key Concepts

### The Chain class

The `Chain` class is at the core of Refiners. It basically lets you express models as a composition of basic layers (linear, convolution, attention, etc) in a **declarative way**.

E.g.: this is how a Vision Transformer (ViT) looks like with Refiners:

```python
import torch
import refiners.fluxion.layers as fl

class ViT(fl.Chain):
    # The Vision Transformer model structure is entirely defined in the constructor. It is
    # ready-to-use right after i.e. no need to implement any forward function or add extra logic
    def __init__(
        self,
        embedding_dim: int = 512,
        patch_size: int = 16,
        image_size: int = 384,
        num_layers: int = 12,
        num_heads: int = 8,
    ):
        num_patches = (image_size // patch_size)
        super().__init__(
            fl.Conv2d(in_channels=3, out_channels=embedding_dim, kernel_size=patch_size, stride=patch_size),
            fl.Reshape(num_patches**2, embedding_dim),
            # The Residual layer implements the so-called skip-connection, i.e. x + F(x).
            # Here the patch embeddings (x) are summed with the position embeddings (F(x)) whose
            # weights are stored in the Parameter layer (note: there is no extra classification
            # token in this toy example)
            fl.Residual(fl.Parameter(num_patches**2, embedding_dim)),
            # These are the transformer encoders:
            *(
                fl.Chain(
                    fl.LayerNorm(embedding_dim),
                    fl.Residual(
                        # The Parallel layer is used to pass multiple inputs to a downstream
                        # layer, here multiheaded self-attention
                        fl.Parallel(
                            fl.Identity(),
                            fl.Identity(),
                            fl.Identity()
                        ),
                        fl.Attention(
                            embedding_dim=embedding_dim,
                            num_heads=num_heads,
                            key_embedding_dim=embedding_dim,
                            value_embedding_dim=embedding_dim,
                        ),
                    ),
                    fl.LayerNorm(embedding_dim),
                    fl.Residual(
                        fl.Linear(embedding_dim, embedding_dim * 4),
                        fl.GeLU(),
                        fl.Linear(embedding_dim * 4, embedding_dim),
                    ),
                    fl.Chain(
                        fl.Linear(embedding_dim, embedding_dim * 4),
                        fl.GeLU(),
                        fl.Linear(embedding_dim * 4, embedding_dim),
                    ),
                )
                for _ in range(num_layers)
            ),
            fl.Reshape(embedding_dim, num_patches, num_patches),
        )

vit = ViT(embedding_dim=768, image_size=224, num_heads=12)  # ~ViT-B/16 like
x = torch.randn(2, 3, 224, 224)
y = vit(x)
```

### The Context API

The `Chain` class has a context provider that allows you to **pass data to layers even when deeply nested**.

E.g. to implement cross-attention you would just need to modify the ViT model like in the toy example below:


```diff
@@ -21,8 +21,8 @@
                     fl.Residual(
                         fl.Parallel(
                             fl.Identity(),
-                            fl.Identity(),
-                            fl.Identity()
+                            fl.UseContext(context="cross_attention", key="my_embed"),
+                            fl.UseContext(context="cross_attention", key="my_embed"),
                         ),  # used to pass multiple inputs to a layer
                         fl.Attention(
                             embedding_dim=embedding_dim,
@@ -49,5 +49,6 @@
         )

 vit = ViT(embedding_dim=768, image_size=224, num_heads=12)  # ~ViT-B/16 like
+vit.set_context("cross_attention", {"my_embed": torch.randn(2, 196, 768)})
 x = torch.randn(2, 3, 224, 224)
 y = vit(x)
```

### The Adapter API

The `Adapter` API lets you **easily patch models** by injecting parameters in targeted layers. It comes with built-in support for canonical adapter types like LoRA, but you can also implement your custom adapters with it.

E.g. to inject LoRA layers in all attention's linear layers:

```python
from refiners.adapters.lora import LoraAdapter

for layer in vit.layers(fl.Attention):
    for linear, parent in layer.walk(fl.Linear):
        adapter = LoraAdapter(target=linear, rank=64, device=vit.device, dtype=vit.dtype)
        adapter.inject(parent)

# ... and load existing weights if the LoRAs are pretrained ...
```

## Getting Started

### Install

```bash
# inference only
pip install refiners
```

Or:

```bash
# inference + training
pip install 'refiners[training]'
```

### Hello World

Here is how to perform a text-to-image inference using the Stable Diffusion 1.5 foundational model patched with a Pokemon LoRA:

Step 1: prepare the model weights in refiners' format:

```bash
python scripts/convert-clip-weights.py --output-file CLIPTextEncoderL.safetensors
python scripts/convert-sd-lda-weights.py --output-file lda.safetensors
python scripts/convert-sd-unet-weights.py --output-file unet.safetensors
```

> Note: this will download the original weights from https://huggingface.co/runwayml/stable-diffusion-v1-5 which takes some time. If you already have this repo cloned locally, use the `--from /path/to/stable-diffusion-v1-5` option instead.

Step 2: download and convert a community Pokemon LoRA, e.g. [this one](https://huggingface.co/pcuenq/pokemon-lora)

```bash
curl -LO https://huggingface.co/pcuenq/pokemon-lora/resolve/main/pytorch_lora_weights.bin
python scripts/convert-lora-weights.py \
  --from pytorch_lora_weights.bin \
  --output-file pokemon_lora.safetensors
```

Step 3: run inference using the GPU:

```python
from refiners.foundationals.latent_diffusion import StableDiffusion_1
from refiners.foundationals.latent_diffusion.lora import LoraWeights
from refiners.fluxion.utils import load_from_safetensors, manual_seed
import torch


sd15 = StableDiffusion_1(device="cuda")
sd15.clip_text_encoder.load_state_dict(load_from_safetensors("CLIPTextEncoderL.safetensors"))
sd15.lda.load_state_dict(load_from_safetensors("lda.safetensors"))
sd15.unet.load_state_dict(load_from_safetensors("unet.safetensors"))

# This uses the LoraAdapter internally and takes care to inject it where it should
lora_weights = LoraWeights("pokemon_lora.safetensors", device=sd15.device)
lora_weights.patch(sd15, scale=1.0)

prompt = "a cute cat"

with torch.no_grad():
    clip_text_embedding = sd15.compute_text_embedding(prompt)

sd15.set_num_inference_steps(30)

manual_seed(2)
x = torch.randn(1, 4, 64, 64, device=sd15.device)

with torch.no_grad():
    for step in sd15.steps:
        x = sd15(
            x,
            step=step,
            clip_text_embedding=clip_text_embedding,
            condition_scale=7.5,
        )
    predicted_image = sd15.lda.decode_latents(x)
    predicted_image.save("pokemon_cat.png")
```

You should get:

![pokemon cat output](https://raw.githubusercontent.com/finegrain-ai/refiners/main/assets/pokemon_cat.png)

## Training

Refiners has a built-in training utils library and provides scripts that can be used as a starting point.

E.g. to train a LoRA on top of Stable Diffusion, copy and edit `configs/finetune-lora.toml` to suit your needs and launch the training as follows:

```bash
python scripts/training/finetune-ldm-lora.py configs/finetune-lora.toml
```

## Credits

We took inspiration from these great projects:

- [tinygrad](https://github.com/tinygrad/tinygrad) - For something between PyTorch and [karpathy/micrograd](https://github.com/karpathy/micrograd)
- [Composer](https://github.com/mosaicml/composer) - A PyTorch Library for Efficient Neural Network Training
- [Keras](https://github.com/keras-team/keras) - Deep Learning for humans

## Citation

```bibtex
@misc{the-finegrain-team-2023-refiners,
  author = {Benjamin Trom and Pierre Chapuis and Cédric Deltheil},
  title = {Refiners: The simplest way to train and run adapters on top of foundational models},
  year = {2023},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/finegrain-ai/refiners}}
}
```
