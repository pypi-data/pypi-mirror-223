import inspect
from typing import Any, Callable, Iterable, Iterator, TypeVar, cast, overload
from torch import Tensor, cat, device as Device, dtype as DType
from refiners.fluxion.layers.basics import Identity
from refiners.fluxion.layers.module import Module, ContextModule, WeightedModule
from refiners.fluxion.context import Contexts, ContextProvider


T = TypeVar("T", bound=Module)
TChain = TypeVar("TChain", bound="Chain")  # because Self (PEP 673) is not in 3.10


class Lambda(Module):
    """Lambda is a wrapper around a callable object that allows it to be used as a PyTorch module."""

    def __init__(self, func: Callable[..., Any]) -> None:
        super().__init__()
        self.func = func

    def forward(self, *args: Any) -> Any:
        return self.func(*args)

    def __repr__(self):
        func_name = getattr(self.func, "__name__", "partial_function")
        return f"Lambda({func_name}{str(inspect.signature(self.func))})"


def generate_unique_names(
    modules: tuple[Module, ...],
) -> dict[str, Module]:
    class_counts: dict[str, int] = {}
    unique_names: list[tuple[str, Module]] = []
    for module in modules:
        class_name = module.__class__.__name__
        class_counts[class_name] = class_counts.get(class_name, 0) + 1
    name_counter: dict[str, int] = {}
    for module in modules:
        class_name = module.__class__.__name__
        name_counter[class_name] = name_counter.get(class_name, 0) + 1
        unique_name = f"{class_name}_{name_counter[class_name]}" if class_counts[class_name] > 1 else class_name
        unique_names.append((unique_name, module))
    return dict(unique_names)


class UseContext(ContextModule):
    structural_attrs = ["context", "key", "func"]

    def __init__(self, context: str, key: str) -> None:
        super().__init__()
        self.context = context
        self.key = key
        self.func: Callable[[Any], Any] = lambda x: x

    def __call__(self, *args: Any) -> Any:
        context = self.use_context(self.context)
        assert context, f"context {self.context} is unset"
        value = context.get(self.key)
        assert value is not None, f"context entry {self.context}.{self.key} is unset"
        return self.func(value)

    def __repr__(self):
        return f"{self.__class__.__name__}(context={repr(self.context)}, key={repr(self.key)})"

    def compose(self, func: Callable[[Any], Any]) -> "UseContext":
        self.func = func
        return self


class SetContext(ContextModule):
    """A Module that sets a context value when executed.

    The context need to pre exist in the context provider.
    #TODO Is there a way to create the context if it doesn't exist?
    """

    structural_attrs = ["context", "key", "callback"]

    def __init__(self, context: str, key: str, callback: Callable[[Any, Any], Any] | None = None) -> None:
        super().__init__()
        self.context = context
        self.key = key
        self.callback = callback

    def __call__(self, x: Tensor) -> Tensor:
        if context := self.use_context(self.context):
            if not self.callback:
                context.update({self.key: x})
            else:
                self.callback(context[self.key], x)

        return x

    def __repr__(self):
        return f"{self.__class__.__name__}(context={repr(self.context)}, key={repr(self.key)})"


class ReturnException(Exception):
    """Exception raised when a Return module is encountered."""

    def __init__(self, value: Tensor):
        self.value = value


class Return(Module):
    """A Module that stops the execution of a Chain when encountered."""

    def forward(self, x: Tensor):
        raise ReturnException(x)


def structural_copy(m: T) -> T:
    return m.structural_copy() if isinstance(m, ContextModule) else m


class Chain(ContextModule):
    _modules: dict[str, Module]
    _provider: ContextProvider

    def __init__(self, *args: Module | Iterable[Module]) -> None:
        super().__init__()
        self._provider = ContextProvider()
        modules = cast(
            tuple[Module],
            (
                tuple(args[0])
                if len(args) == 1 and isinstance(args[0], Iterable) and not isinstance(args[0], Chain)
                else tuple(args)
            ),
        )

        for module in modules:
            # Violating this would mean a ContextModule ends up in two chains,
            # with a single one correctly set as its parent.
            assert (
                (not isinstance(module, ContextModule))
                or (not module._can_refresh_parent)
                or (module.parent is None)
                or (module.parent == self)
            ), f"{module.__class__.__name__} already has parent {module.parent.__class__.__name__}"

        self._regenerate_keys(modules)
        self._reset_context()

        for module in self:
            if isinstance(module, ContextModule) and module._can_refresh_parent and module.parent != self:
                module._set_parent(self)

    @property
    def provider(self) -> ContextProvider:
        return self._provider

    def init_context(self) -> Contexts:
        return {}

    def _register_provider(self, context: Contexts | None = None) -> None:
        if context:
            self._provider.update_contexts(context)

        for module in self:
            if isinstance(module, Chain):
                module._register_provider(context=self._provider.contexts)

    def _reset_context(self) -> None:
        self._register_provider(self.init_context())

    def set_context(self, context: str, value: Any) -> None:
        self._provider.set_context(context, value)
        self._register_provider()

    def debug_repr(self, layer_name: str = "") -> str:
        lines: list[str] = []
        tab = "  "
        tab_length = 0
        for i, parent in enumerate(self.get_parents()[::-1]):
            lines.append(f"{tab*tab_length}{'└─ ' if i else ''}{parent.__class__.__name__}")
            tab_length += 1

        lines.append(f"{tab*tab_length}└─ {self.__class__.__name__}")

        for name, _ in self._modules.items():
            error_arrow = "⚠️" if name == layer_name else ""
            lines.append(f"{tab*tab_length} | {name} {error_arrow}")

        return "\n".join(lines)

    def call_layer(self, layer: Module, layer_name: str, *args: Any):
        try:
            return layer(*args)
        except Exception as e:
            pretty_print = self.debug_repr(layer_name)
            raise ValueError(f"Error in layer {layer_name}, args:\n {args}\n \n{pretty_print}") from e

    def forward(self, *args: Any) -> Any:
        result: tuple[Any] | Any = None
        intermediate_args: tuple[Any, ...] = args
        for name, layer in self._modules.items():
            result = self.call_layer(layer, name, *intermediate_args)
            intermediate_args = (result,) if not isinstance(result, tuple) else result

        self._reset_context()
        return result

    def _regenerate_keys(self, modules: Iterable[Module]) -> None:
        self._modules = generate_unique_names(tuple(modules))  # type: ignore

    def __add__(self, other: "Chain | Module | list[Module]") -> "Chain":
        if isinstance(other, Module):
            other = Chain(other)
        if isinstance(other, list):
            other = Chain(*other)
        return Chain(*self, *other)

    def __getitem__(self, key: int | str | slice) -> Module:
        if isinstance(key, slice):
            return Chain(*list(self)[key])
        elif isinstance(key, str):
            return self._modules[key]
        else:
            return list(self)[key]

    def __iter__(self) -> Iterator[Module]:
        return iter(self._modules.values())

    def _pretty_print(self, num_tab: int = 0, layer_name: str | None = None) -> str:
        layer_name = self.__class__.__name__ if layer_name is None else layer_name
        pretty_print = f"{layer_name}:\n"
        tab = " " * (num_tab + 4)
        module_strings: list[str] = []
        for i, (name, module) in enumerate(self._modules.items()):
            ident = ("└+" if isinstance(self, Sum) else "└─") if i == 0 else "  "
            module_str = (
                module
                if not isinstance(module, Chain)
                else (module._pretty_print(len(tab), name) if num_tab < 12 else f"{name}(...)")
            )
            module_strings.append(f"{tab}{ident} {module_str}")
        pretty_print += "\n".join(module_strings)
        return pretty_print

    def __repr__(self) -> str:
        return self._pretty_print()

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} at {hex(id(self))}>"

    def __len__(self) -> int:
        return len(self._modules)

    @property
    def device(self) -> Device | None:
        wm = self.find(WeightedModule)
        return None if wm is None else wm.device

    @property
    def dtype(self) -> DType | None:
        wm = self.find(WeightedModule)
        return None if wm is None else wm.dtype

    def _walk(self, predicate: Callable[[Module, "Chain"], bool] | None = None) -> Iterator[tuple[Module, "Chain"]]:
        if predicate is None:
            predicate = lambda _m, _p: True
        for module in self:
            keep_going = True
            try:
                p = predicate(module, self)
            except StopIteration:
                p = False
                keep_going = False
            if p:
                yield (module, self)
            if keep_going and isinstance(module, Chain):
                yield from module.walk(predicate)

    @overload
    def walk(self, predicate: Callable[[Module, "Chain"], bool] | None = None) -> Iterator[tuple[Module, "Chain"]]:
        ...

    @overload
    def walk(self, predicate: type[T]) -> Iterator[tuple[T, "Chain"]]:
        ...

    def walk(
        self, predicate: type[T] | Callable[[Module, "Chain"], bool] | None = None
    ) -> Iterator[tuple[T, "Chain"]] | Iterator[tuple[Module, "Chain"]]:
        if isinstance(predicate, type):
            return self._walk(lambda m, _: isinstance(m, predicate))
        else:
            return self._walk(predicate)

    def layers(self, layer_type: type[T]) -> Iterator[T]:
        for module, _ in self.walk(layer_type):
            yield module

    def find(self, layer_type: type[T]) -> T | None:
        return next(self.layers(layer_type=layer_type), None)

    def find_parent(self, module: Module) -> "Chain | None":
        if module in self:  # avoid DFS-crawling the whole tree
            return self
        for _, parent in self.walk(lambda m, _: m == module):
            return parent
        return None

    def insert(self, index: int, module: Module) -> None:  # type: ignore
        if index < 0:
            index = max(0, len(self._modules) + index + 1)
        modules = list(self)
        modules.insert(index, module)
        self._regenerate_keys(modules)
        if isinstance(module, ContextModule):
            module._set_parent(self)
        self._register_provider()

    def insert_after_type(self, module_type: type[Module], new_module: Module) -> None:
        for i, module in enumerate(self):
            if isinstance(module, module_type):
                self.insert(i + 1, new_module)
                return
        raise ValueError(f"No module of type {module_type.__name__} found in the chain.")

    def append(self, module: Module) -> None:  # type: ignore
        modules = list(self)
        modules.append(module)
        self._regenerate_keys(modules)
        if isinstance(module, ContextModule):
            module._set_parent(self)
        self._register_provider()

    def pop(self, index: int = -1) -> Module | tuple[Module]:  # type: ignore
        modules = list(self)
        if index < 0:
            index = len(modules) + index
        if index < 0 or index >= len(modules):
            raise IndexError("Index out of range.")
        removed_module = modules.pop(index)
        if isinstance(removed_module, ContextModule):
            removed_module._set_parent(None)
        self._regenerate_keys(modules)
        return removed_module

    def remove(self, module: Module) -> None:
        """Remove a module from the chain."""
        modules = list(self)
        try:
            modules.remove(module)
        except ValueError:
            raise ValueError(f"{module} is not in {self}")
        self._regenerate_keys(modules)
        if isinstance(module, ContextModule):
            module._set_parent(None)

    def replace(
        self,
        old_module: Module,
        new_module: Module,
        old_module_parent: "Chain | None" = None,
    ) -> None:
        """Replace a module in the chain with a new module."""
        modules = list(self)
        try:
            modules[modules.index(old_module)] = new_module
        except ValueError:
            raise ValueError(f"{old_module} is not in {self}")
        self._regenerate_keys(modules)
        if isinstance(new_module, ContextModule):
            new_module._set_parent(self)
        if isinstance(old_module, ContextModule):
            old_module._set_parent(old_module_parent)

    def structural_copy(self: TChain) -> TChain:
        """Copy the structure of the Chain tree.

        This method returns a recursive copy of the Chain tree where all inner nodes
        (instances of Chain and its subclasses) are duplicated and all leaves
        (regular Modules) are not.

        Such copies can be adapted without disrupting the base model, but do not
        require extra GPU memory since the weights are in the leaves and hence not copied.

        This assumes all subclasses define the class variable `structural_attrs` which
        contains a list of basic attributes set in the constructor. In complicated cases
        it may be required to overwrite that method.
        """
        if hasattr(self, "_pre_structural_copy"):
            self._pre_structural_copy()

        modules = [structural_copy(m) for m in self]

        # Instantiate the right subclass, but do not initialize.
        clone = object.__new__(self.__class__)

        # Copy all basic attributes of the class declared in `structural_attrs`.
        for k in self.__class__.structural_attrs:
            setattr(clone, k, getattr(self, k))

        # Call constructor of Chain, which among other things refreshes the context tree.
        Chain.__init__(clone, *modules)

        for module in modules:
            if isinstance(module, ContextModule):
                module._set_parent(clone)

        if hasattr(clone, "_post_structural_copy"):
            clone._post_structural_copy(self)

        return clone


class Parallel(Chain):
    def forward(self, *args: Any) -> tuple[Tensor, ...]:
        return tuple([self.call_layer(module, name, *args) for name, module in self._modules.items()])


class Distribute(Chain):
    def forward(self, *args: Any) -> tuple[Tensor, ...]:
        assert len(args) == len(self._modules), "Number of positional arguments must match number of sub-modules."
        return tuple([self.call_layer(module, name, arg) for arg, (name, module) in zip(args, self._modules.items())])


class Passthrough(Chain):
    def forward(self, *inputs: Any) -> Any:
        super().forward(*inputs)
        return inputs


class Sum(Chain):
    def forward(self, *inputs: Any) -> Any:
        output = None
        for layer in self:
            layer_output: Any = layer(*inputs)
            if isinstance(layer_output, tuple):
                layer_output = sum(layer_output)  # type: ignore
            output = layer_output if output is None else output + layer_output
        return output


class Residual(Sum):
    def __init__(self, *modules: Module) -> None:
        super().__init__(Identity(), Chain(*modules))


class Breakpoint(Module):
    def __init__(self, vscode: bool = True):
        super().__init__()
        self.vscode = vscode

    def forward(self, *args: Any):
        if self.vscode:
            import debugpy  # type: ignore

            debugpy.breakpoint()  # type: ignore
        else:
            breakpoint()
        return args[0] if len(args) == 1 else args


class Concatenate(Chain):
    structural_attrs = ["dim"]

    def __init__(self, *modules: Module, dim: int = 0) -> None:
        super().__init__(*modules)
        self.dim = dim

    def forward(self, *args: Any) -> Tensor:
        outputs = [module(*args) for module in self]
        return cat([output for output in outputs if output is not None], dim=self.dim)
