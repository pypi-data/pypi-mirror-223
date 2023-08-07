from __future__ import annotations

import logging
import sys
import time
from typing import Any
from pathlib import Path
from shutil import copy
import os


from forum.topic import TOPIC, TopicFowarder
from forum.config import Config
from forum.plugin.node import NodeFactory, NodeManager
from forum.plugin import plugin_loader
from forum.plugin.node import Node
import forum

CONFIG_LOCATION = "~/.local/share/byte/config.yml"
CONFIG_TEMPLATE_NAME = 'config.yml.template'

def initialize_config(
    telegram_api_key,
    llm_location,
    io_language,
):
    config_location = Path(CONFIG_LOCATION).absolute()
    module_location = Path(forum.__file__).parent.absolute()
    config_template_location = module_location / CONFIG_TEMPLATE_NAME

    config_template = config_template_location.read_text()
    config_template = config_template.format(
        telegram_api_key=telegram_api_key,
        llm_location=llm_location,
        io_language=io_language,
    )
    if not config_location.is_file():
        config_location.parent.mkdir(parents=True,exist_ok=True)
        config_location.write_text(config_template)


def load_nodes(
    node_factory: NodeFactory, nodes_configs: dict[str, dict[str, Any]]
) -> list[tuple[str, Node]]:
    nodes = []
    for name, config in nodes_configs.items():
        logging.info(f"Initializing service: {name}({config})")
        node_type = config.pop("type")
        node = node_factory.create(node_type, **config)
        nodes.append((name, node))
    return nodes


def map_topics(topics_map: dict[str, str | list[str]]) -> None:
    for input_topic, output_topics in topics_map.items():
        if isinstance(output_topics, str):
            output_topics = [output_topics]

        for output_topic in output_topics:
            logging.info(f"Fowarding: {input_topic} -> {output_topic}")
            fowarder = TopicFowarder(output_topic)
            TOPIC.subscribe(input_topic, fowarder)


def main(config_location: str):
    logging.basicConfig(level=logging.INFO)

    config = Config.from_yaml(config_location)
    logging.info(f"Loaded config: {config}")

    plugin_facotories = plugin_loader.load_plugins(config.plugins)
    nodes_factory: NodeFactory = plugin_facotories[Node]  # type: ignore
    nodes = load_nodes(nodes_factory, config.nodes)
    node_manager = NodeManager()
    for name, node in nodes:
        node_manager.add_node(name, node)
    map_topics(config.topics)

    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        logging.info("🚪 Exiting")
    finally:
        TOPIC.shutdown()
        sys.exit(0)

def get_config_file_location() -> Path:
    user_home = os.environ.get('HOME')
    user_home = Path(user_home)
    default_config_dir_location = user_home/'.byte'
    default_config_file_location = default_config_dir_location / 'config.yml'
    config_file_location = os.environ.get('BYTE_CONFIG', default_config_file_location)
    config_file_location = Path(config_file_location)
    return config_file_location

if __name__ == "__main__":
    # init_params = (
    #     'telegram_api_key',
    #     'llm_location',
    #     'io_language',
    # )
    # init_param_values = {}
    # for init_param in init_params:
    #     init_param_values[init_param] = input(f'Value for {init_param}:')

    # initialize_config(
    #     **init_param_values
    # )
    
    config_file_location = get_config_file_location()
    
    # if not config_file_location.is_file():
    #     config_location = Path(CONFIG_LOCATION).absolute()
    #     module_location = Path(byte.__file__).parent.absolute()
    #     config_template_location = module_location / CONFIG_TEMPLATE_NAME
    
    main('/home/red/repos/byte/config.yml')
