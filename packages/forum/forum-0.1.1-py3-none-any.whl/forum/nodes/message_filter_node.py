from typing import ClassVar, Mapping
from forum.nodes.chat_message import ChatMessage
from pydantic.dataclasses import dataclass


# this can be waaaaay more generic
# plz refactor
@dataclass
class Plugin:
    TYPE: ClassVar[str] = "message_filter"
    content_type: str | None = None

    def callback(self, message: Mapping, context: Mapping):
        chat_message = ChatMessage(**message)

        if self.content_type and self.content_type != chat_message.type:
            return

        return chat_message.dict()
