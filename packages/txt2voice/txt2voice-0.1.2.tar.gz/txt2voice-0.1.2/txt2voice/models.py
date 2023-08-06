"""
Models for txt2voice app
"""

from typing import Optional
from pydantic import BaseModel


class VoiceParams(BaseModel):  # pylint: disable=too-few-public-methods
    """Voice params for Yandex SpeechKit Cloud API"""

    male: Optional[str] = "filipp"
    female: Optional[str] = "alyona"


class SpeedParams(BaseModel):  # pylint: disable=too-few-public-methods
    """Speed params for Yandex SpeechKit Cloud API"""

    speed: float


class RequestParams(BaseModel):  # pylint: disable=too-few-public-methods
    """Request params for Yandex SpeechKit Cloud API"""

    voice: VoiceParams
    speed: SpeedParams
    path_to_audiofiles: str
    folder_id: str
    iam_token: str
    lang: str = "ru-RU"
    text: str


class AudioContent(BaseModel):  # pylint: disable=too-few-public-methods
    """Audio content from Yandex SpeechKit Cloud API"""

    content: bytes
