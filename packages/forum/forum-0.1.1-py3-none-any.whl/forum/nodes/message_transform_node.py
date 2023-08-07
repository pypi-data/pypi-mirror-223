import logging
from typing import ClassVar, Mapping
from forum.nodes.chat_message import ChatMessage
from pydantic.dataclasses import dataclass


@dataclass
class Plugin:
    TYPE: ClassVar[str] = "message_transform"
    rename_fields: dict | None = None
    delete_fields: list | None = None
    set_fields: dict | None = None
    copy_fields: dict | None = None
    output_fields: list | None = None

    def callback(self, message: Mapping, context: Mapping):
        message = dict(message)

        # Review what happens when expressed fields doesnt exit
        # for now nothing happens, this is not a good idea for observability
        # this might be a setting

        if self.rename_fields is not None:
            for original_field_name, new_field_name in self.rename_fields.items():
                # think about what should happend when original field doesent exist
                message[new_field_name] = message.pop(original_field_name)

        if self.delete_fields is not None:
            for field_name in self.delete_fields:
                message.pop(field_name)

        if self.set_fields is not None:
            for field_name, value in self.set_fields.items():
                message[field_name] = value

        if self.copy_fields is not None:
            for original_field_name, new_field_name in self.copy_fields.items():
                message[new_field_name] = message[original_field_name]

        if self.output_fields:
            output_message = {}
            for output_field in self.output_fields:
                if output_field not in message:
                    logging.error(f"Missing output field {output_field} in message")
                    return
                output_message[output_field] = message[output_field]
            message = output_message

        return message
