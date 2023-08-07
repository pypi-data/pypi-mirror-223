from typing import Protocol, runtime_checkable
from forum.plugin.protocol import Plugin as PluginProtocol


@runtime_checkable
class PluginModule(Protocol):
    Plugin: PluginProtocol
