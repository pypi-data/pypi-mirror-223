from typing import ClassVar, Mapping, Protocol, runtime_checkable


@runtime_checkable
class Node(Protocol):
    TYPE: ClassVar[str]

    def callback(
        self, message: Mapping, context: Mapping | None = None
    ) -> Mapping | None:
        ...

    def __call__(self, *args, **kwargs):
        ...


@runtime_checkable
class ContextBuilder(Protocol):
    def build_context(self, instance_name: str) -> Mapping | None:
        ...


@runtime_checkable
class ContextDestroyer(Protocol):
    def destroy_context(self, context: Mapping) -> None:
        ...
