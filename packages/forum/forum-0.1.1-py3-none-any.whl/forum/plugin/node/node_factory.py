"""Factory for creating a registered."""
from __future__ import annotations

import logging
from typing import Callable, ClassVar, MutableMapping
from dataclasses import dataclass, field
from forum.plugin import Plugin
from forum.plugin.node.node import Node


@dataclass(slots=True)
class NodeFactory:
    _creation_funcs: ClassVar[MutableMapping[str, Callable]] = {}

    def register(self, type_name: str, creator_fn: Callable) -> None:
        """Register a new registered type."""
        self._creation_funcs[type_name] = creator_fn

    def unregister(self, type_name: str) -> None:
        """Unregister a registered type."""
        self._creation_funcs.pop(type_name, None)

    def create(self, type_name: str, **kwargs) -> Node:
        """Create a registered of a specific type"""
        try:
            creator_func = self._creation_funcs[type_name]
        except KeyError:
            raise ValueError(f"Unknown registered type {type_name!r}") from None
        logging.info("Exec creator function: %s(%s)", type_name, kwargs)
        return creator_func(**kwargs)
