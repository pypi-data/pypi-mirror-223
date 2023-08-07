from __future__ import annotations

from dataclasses import field
from pathlib import Path
from typing import Any
from pydantic import BaseModel
from forum.plugin.node import Node

import yaml


# @dataclass
class Config(BaseModel):
    # Warning this are not class atributes and dont use
    # a default_factory because of pydantict
    # please see https://stackoverflow.com/questions/63793662/how-to-give-a-pydantic-list-field-a-default-value
    plugins: list[str] = []
    nodes: dict[str, dict[str, Any]] = {}
    topics: dict[str, str | list[str]] = {}

    @classmethod
    def from_yaml(cls, yaml_location: str):
        config_location = Path(yaml_location)

        with config_location.open(encoding="utf-8") as config_file:
            config_data = yaml.safe_load(config_file)

        return cls(**config_data)
