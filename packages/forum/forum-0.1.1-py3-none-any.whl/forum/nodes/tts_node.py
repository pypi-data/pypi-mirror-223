from __future__ import annotations

import time
from pathlib import Path
from typing import ClassVar, Mapping

import requests
from pydantic import BaseModel
from pydantic.dataclasses import dataclass


class TTSAPI(BaseModel):
    address: str
    port: int

    def request_tts(self, prompt: str) -> str:
        endpoint = f"http://{self.address}:{self.port}/tts"
        message = {"text": prompt}
        response = requests.post(endpoint, json=message, timeout=300)
        current_time = time.time()
        audio_file_location = Path(f"{current_time}_tts_response.wav").absolute()
        with audio_file_location.open("wb") as audio_file:
            audio_file.write(response.content)

        return str(audio_file_location)


class TTSContext(BaseModel):
    tts_api: TTSAPI


class TTSMessage(BaseModel):
    text: str


class TTSResponse(BaseModel):
    file_location: str


@dataclass
class Plugin:
    TYPE: ClassVar[str] = "tts"
    address: str
    port: int

    def build_context(self, instance_name: str) -> Mapping:
        tts_api = TTSAPI(address=self.address, port=self.port)
        tts_context = TTSContext(tts_api=tts_api)
        return tts_context.dict()

    def callback(self, message: Mapping, context: Mapping):
        tts_message = TTSMessage(**message)
        tts_contex = TTSContext(**context)
        tts_api = tts_contex.tts_api
        response_data = tts_api.request_tts(tts_message.text)
        tts_response = TTSResponse(file_location=response_data)

        return tts_response.dict()
