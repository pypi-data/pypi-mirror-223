from typing import Any, Mapping
from pydantic import BaseModel


class ChatMessage(BaseModel):
    chat_id: str
    input_message_id: str
    type: str
    content: str
