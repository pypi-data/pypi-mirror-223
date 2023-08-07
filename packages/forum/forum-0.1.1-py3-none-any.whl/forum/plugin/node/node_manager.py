import logging
from typing import Any, Mapping, MutableMapping

from forum.plugin.node.node import ContextBuilder, ContextDestroyer, Node
from forum.topic import TOPIC


class NodeCallbackAdapter:
    def __init__(self, name: str, node: Node):
        self.name = name
        self.input_topic = f"{name}.input"
        self.output_topic = f"{name}.output"
        self.callback = node.callback
        self.context = None

        if isinstance(node, ContextBuilder):
            self.context = node.build_context(name)

    def __call__(self, message: Mapping):
        response = self.callback(message, self.context)
        if response is not None:
            TOPIC.publish(self.output_topic, response)

    def __repr__(self) -> str:
        return f"NodeCallbackAdapter(name={self.name})"


class NodeManager:
    def __init__(self) -> None:
        self.nodes: MutableMapping[str, Node] = {}
        self.nodes_context: MutableMapping[str, Any] = {}

    def add_node(self, name: str, node: Node):
        self.nodes[name] = node
        node_callback_adapter = NodeCallbackAdapter(name, node)
        if node_callback_adapter is not None:
            self.nodes_context[name] = node_callback_adapter.context
        TOPIC.subscribe(
            node_callback_adapter.input_topic,
            node_callback_adapter,
        )

    def remove_node(self, name: str):
        try:
            node = self.nodes[name]
        except KeyError as key_error:
            raise RuntimeError(
                f"Failed to remove node {name}, node not found"
            ) from key_error

        if not isinstance(node, ContextDestroyer):
            return

        try:
            node_context = self.nodes_context[name]
            node.destroy_context(**node_context)
        except KeyError as key_error:
            raise RuntimeError(
                f"Failed to destroy context for {name}, node context not found"
            ) from key_error
