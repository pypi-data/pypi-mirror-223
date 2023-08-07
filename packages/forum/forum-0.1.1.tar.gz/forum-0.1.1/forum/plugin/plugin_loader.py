"""A simple plugin loader.
from https://github.com/ArjanCodes/2021-plugin-architecture/blob/main/after/game/loader.py
"""
from __future__ import annotations

import importlib
import logging
from types import ModuleType
from typing import Mapping, Protocol

from forum.plugin.node import Node, NodeFactory
from forum.plugin import Plugin, PluginFactory, PluginModule

FACTORIES_MAPPING: Mapping[Plugin, PluginFactory] = {Node: NodeFactory()}


class PluginRegisterer:
    interface: Protocol
    factory: object


def import_module(name: str) -> ModuleType | None:
    """Imports a module given a name."""
    try:
        module = importlib.import_module(name)  # type: ignore
    except (ModuleNotFoundError, ImportError) as exeption:
        logging.error(f"Failed to import module {name}, {exeption}")
        module = None
    return module


def register_plugin(module: PluginModule):
    for protocol, factory in FACTORIES_MAPPING.items():
        plugin = module.Plugin
        if isinstance(plugin, protocol):  # type: ignore
            return factory.register(plugin.TYPE, plugin)
    logging.error(
        "Unsuported plugin type, must confome with one of the following "
        f"protocols: {FACTORIES_MAPPING.keys()}"
    )


def load_plugins(plugins: list[str]) -> Mapping[Plugin, PluginFactory]:
    """Loads the plugins defined in the plugins list."""
    n_plugins = len(plugins)
    logging.info(f"🔌 Plugins found: {n_plugins}")

    for plugin_file in plugins:
        module = import_module(plugin_file)
        if not isinstance(module, PluginModule):
            logging.info(
                f"❌ Failed to load {plugin_file} plugin, it does not respect the PluginModule protocol"
            )
            continue
        register_plugin(module)
        logging.info(f"✔️ Loaded {plugin_file} plugin")

    return dict(FACTORIES_MAPPING)
