from typing import Callable, Protocol, runtime_checkable

from forum.plugin.protocol import Plugin


@runtime_checkable
class PluginFactory(Protocol):
    def register(self, type_name: str, creator_fn: Callable) -> None:
        """Unregisters a register type."""
        ...

    def unregister(self, type_name: str) -> None:
        """Unregisters a registered type."""
        ...

    def create(self, type_name: str, **kwargs) -> Plugin:
        """Creates object of given type."""
        ...
