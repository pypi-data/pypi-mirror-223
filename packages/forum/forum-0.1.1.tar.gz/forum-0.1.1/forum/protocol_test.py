from dataclasses import dataclass
from inspect import signature
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
class InstanceAware(Protocol):
    def __init__(self, instance_name: str, *args, **kwargs) -> None:
        ...


@dataclass
class Plugin:
    TYPE: ClassVar[str] = "telegram_bot"
    api_key: str

    def callback(self, message: Mapping, context: Mapping):
        pass


parameter = signature(Plugin.__init__).parameters.keys()
print("is node:", isinstance(Plugin, Node))
print("is instance aware:", issubclass(Plugin, InstanceAware))
