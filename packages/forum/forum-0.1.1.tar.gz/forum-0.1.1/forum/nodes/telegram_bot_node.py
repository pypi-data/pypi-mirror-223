from functools import partial
import logging
from threading import Thread
from typing import ClassVar, Mapping

import telebot
from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from telebot.types import Message as TelegramMessage

from forum.topic import TOPIC
from forum.nodes.chat_message import ChatMessage


@dataclass
class TelegramBotAPI:
    def __init__(self, instance_name: str, api_key: str):
        self._instance_name = instance_name
        self.bot = telebot.TeleBot(api_key)

        handlers_output_topic = f"{instance_name}.output"
        chat_start_handler = partial(self.chat_start_handler, handlers_output_topic)
        self.bot.register_message_handler(
            chat_start_handler, commands=["help", "start"]
        )

        chat_text_handler = partial(self.chat_text_handler, handlers_output_topic)
        self.bot.register_message_handler(chat_text_handler, content_types=["text"])

        audio_message_handler = partial(
            self.audio_message_handler, handlers_output_topic
        )
        self.bot.register_message_handler(
            audio_message_handler, content_types=["voice"]
        )
        self.pooling_thread = Thread(
            name="telebot_pooling",
            target=self.bot.infinity_polling,
        )

    @staticmethod
    def chat_start_handler(output_topic: str, telegram_message: TelegramMessage):
        greeting_text = "Bom dia, tudo bem?"
        text_message = ChatMessage(
            chat_id=str(telegram_message.chat.id),
            input_message_id=str(telegram_message.id),
            type="text",
            content=greeting_text,
        )

        TOPIC.publish(output_topic, text_message.dict())

    @staticmethod
    def chat_text_handler(output_topic: str, telegram_message: TelegramMessage):
        logging.info("TEXT RECIVED")
        if not telegram_message.text:
            return

        text_message = ChatMessage(
            chat_id=str(telegram_message.chat.id),
            input_message_id=str(telegram_message.id),
            type="text",
            content=telegram_message.text,
        )

        TOPIC.publish(output_topic, text_message.dict())

    @staticmethod
    def audio_message_handler(output_topic: str, telegram_message: TelegramMessage):
        response_text = "Amo esse som!"
        text_message = ChatMessage(
            chat_id=str(telegram_message.chat.id),
            input_message_id=str(telegram_message.id),
            type="text",
            content=response_text,
        )

        TOPIC.publish(output_topic, text_message.dict())

    def send_message(self, chat_message: ChatMessage):
        if chat_message.type == "text":
            chat_id = int(chat_message.chat_id)
            self.bot.send_message(
                chat_id,
                chat_message.content,
            )
        else:
            raise RuntimeError("Invalid message type")

    def start(self):
        self.pooling_thread.start()

    def shutdown(self, timeout_seconds: float = 5):
        self.pooling_thread.join(timeout=timeout_seconds)


class TelegramContext(BaseModel):
    telegram_api: TelegramBotAPI


@dataclass
class Plugin:
    TYPE: ClassVar[str] = "telegram_bot"
    api_key: str

    def build_context(self, instance_name: str) -> Mapping:
        logging.info("telegram context created")
        telegram_api = TelegramBotAPI(instance_name, self.api_key)

        telegram_api.start()
        telegram_context = TelegramContext(telegram_api=telegram_api)
        return telegram_context.dict()

    def callback(self, message: Mapping, context: Mapping):
        telegram_context = TelegramContext(**context)
        telegram_api = telegram_context.telegram_api
        chat_message = ChatMessage(**message)
        telegram_api.send_message(chat_message)

    def destroy_context(self, context: Mapping):
        telegram_context = TelegramContext(**context)
        telegram_context.telegram_api.shutdown()
