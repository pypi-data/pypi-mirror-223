from typing import Protocol, runtime_checkable


@runtime_checkable
class Plugin(Protocol):
    TYPE: str

    def __call__(self, *args, **kwargs):
        ...
