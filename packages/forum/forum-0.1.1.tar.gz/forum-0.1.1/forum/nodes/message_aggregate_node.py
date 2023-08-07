from dataclasses import field
import logging
from typing import ClassVar, Mapping
from pydantic.dataclasses import dataclass


@dataclass
class Plugin:
    TYPE: ClassVar[str] = "message_aggregate"
    by: list
    output_fields: list
    prioritize: str = "last"
    _aggregation_context: dict = field(default_factory=dict)

    def __post_init__(self):
        # can be implemented with pydantic in a cleaner way
        assert self.prioritize in {
            "last",
            "first",
        }, "Invalid priorization method"

    def callback(self, message: Mapping, context: Mapping):
        message = dict(message)
        merge_key = []

        for merge_by_field in self.by:
            if merge_by_field not in message:
                return
            merge_key.append(message[merge_by_field])

        merge_key = tuple(merge_key)
        if merge_key not in self._aggregation_context:
            self._aggregation_context[merge_key] = message
            return

        first_message = self._aggregation_context.pop(merge_key)
        last_message = message
        output_message = {}

        for output_field in self.output_fields:
            in_first = output_field in first_message
            in_last = output_field in last_message

            match (in_first, in_last, self.prioritize):
                case (True, False, _) | (True, True, "first"):
                    field_value = first_message[output_field]
                case (False, True, _) | (True, True, "last"):
                    field_value = last_message[output_field]
                case (False, False, _):
                    logging.error(
                        f"Missing output field {output_field} in both messages, "
                        f"unable to aggregate first message: {first_message} and last message: {last_message}"
                    )
                    return
                case _:
                    logging.error(
                        f"Well thats unexpected, you should probly take a look at this {(in_first, in_last, self.prioritize) = }"
                    )
                    return

            output_message[output_field] = field_value

        return output_message
