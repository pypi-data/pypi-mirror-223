from copy import copy
from queue import Queue
from threading import Lock, Thread
from typing import Any, Callable, Mapping, MutableMapping
from dataclasses import dataclass
from venv import logger


class CallableList(list[Callable]):
    def __call__(self, *args: Any, **kwargs: Any):
        for item in self:
            item(*args, **kwargs)


SubscriberMap = MutableMapping[str, CallableList]


class PubSub:
    def __init__(self):
        # Locked added as an precaution for more information visit
        # https://github.com/google/styleguide/blob/91d6e367e384b0d8aaaf7ce95029514fcdf38651/pyguide.md#218-threading
        self._subscribers_lock = Lock()
        self.subscribers: SubscriberMap = {}
        self.queue: Queue = Queue()
        self.message_processing_thread = Thread(target=self._process_messages)

    def subscribe(self, subscription_topic: str, callback: Callable):
        with self._subscribers_lock:
            if subscription_topic not in self.subscribers:
                self.subscribers[subscription_topic] = CallableList()

            self.subscribers[subscription_topic].append(callback)

    def publish(self, destination_topic: str, message: Mapping | None):
        if message is not None:
            self.queue.put((destination_topic, message))

    def _process_messages(self):
        while True:
            destination_topic, message = self.queue.get()
            logger.info(f"[{destination_topic}]: {message}")

            if not destination_topic in self.subscribers:
                continue

            with self._subscribers_lock:
                # A shallow copy is made so changes in this subscribers
                # CallableList wont cause trouble this must be refectored
                # to achive better perfomance in topic comunication since
                # it wont scale well
                topic_callbacks = copy(self.subscribers[destination_topic])

            topic_callbacks(message)

    def start(self):
        self.message_processing_thread.start()

    def shutdown(self):
        self.queue.join()
        self.message_processing_thread.join()


@dataclass
class TopicFowarder:
    output_topic: str

    def __call__(self, message: Mapping) -> Any:
        TOPIC.publish(self.output_topic, message)


TOPIC = PubSub()
TOPIC.start()
