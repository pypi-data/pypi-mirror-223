import json
from pathlib import Path
from typing import ClassVar, Mapping
from pydantic.dataclasses import dataclass

import requests
from pydantic import BaseModel


class STTAPI(BaseModel):
    address: str
    port: int
    language: str

    def request_transcription(self, file_location: str | Path) -> str | None:
        endpoint = f"http://{self.address}:{self.port}/stt"
        audio_file_location = Path(file_location)
        stt_request = {"language": "pt"}

        with open(file_location, "rb") as speach_file:
            response = requests.post(
                url=endpoint,
                data={"stt_request": json.dumps(stt_request)},
                files={
                    "audio_file": (audio_file_location.name, speach_file, "audio/wav")
                },
                timeout=30,
            )

        response = response.json()
        response["text"] = response["text"].strip().lower()
        return response["text"]


class STTContext(BaseModel):
    stt_api: STTAPI


class STTMessage(BaseModel):
    file_location: str


class STTResponse(BaseModel):
    text: str | None


@dataclass
class Plugin:
    TYPE: ClassVar[str] = "stt"
    address: str
    port: int
    language: str

    def build_context(self, instance_name: str) -> Mapping:
        stt_api = STTAPI(address=self.address, port=self.port, language=self.language)
        stt_context = STTContext(stt_api=stt_api)
        return stt_context.dict()

    def callback(self, message: Mapping, context: Mapping):
        stt_message = STTMessage(**message)
        stt_contex = STTContext(**context)
        stt_api = stt_contex.stt_api
        response_data = stt_api.request_transcription(stt_message.file_location)
        stt_response = STTResponse(text=response_data)

        return stt_response.dict()
