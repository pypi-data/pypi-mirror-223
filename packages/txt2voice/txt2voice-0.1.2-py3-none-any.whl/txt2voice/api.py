"""
Convert text to voice using Yandex SpeechKit Cloud API.
"""

import typing as t
import aiohttp
from aiohttp.client_exceptions import ClientResponseError
from pydub import AudioSegment  # type: ignore

from txt2voice.models import RequestParams, AudioContent


class TextToVoice:
    """Text to voice converter using Yandex SpeechKit Cloud API."""

    def __init__(self, url: str):
        self.url = url

    async def request_audio_content(self, params: RequestParams) -> t.Optional[AudioContent]:
        """
        Make request to Yandex SpeechKit Cloud API and return audio content.

        Arguments:
            params {RequestParams} -- request params for Yandex SpeechKit Cloud API
        """

        headers = {"Authorization": f"Bearer {params.iam_token}"}

        data = {
            "text": params.text,
            "lang": params.lang,
            "voice": params.voice.male,
            "folderId": params.folder_id,
            "speed": params.speed.speed,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, headers=headers, data=data, ssl=False) as response:
                try:
                    if response.status != 200:
                        raise ValueError(
                            f"Error occurred during the request. Status: {response.status}."
                        )
                    content = await response.content.read()
                    return AudioContent(content=content)
                except ClientResponseError as ex:
                    print(f"Invalid response received: code: {ex.status}")

        return None

    async def save_audio_to_file(self, params: RequestParams):
        """
        Save audio content to file.

        Arguments:
            params {RequestParams} -- request params for Yandex SpeechKit Cloud API
        """

        audio_content: t.Optional[AudioContent] = await self.request_audio_content(params)
        if audio_content:
            with open(params.path_to_audiofiles, "wb") as file:
                file.write(audio_content.content)
        else:
            raise ValueError("Audio content is empty.")

    @staticmethod
    def convert_ogg_to_mp3(input_file, output_file):
        """
        Convert ogg file to mp3.

        Arguments:
            input_file {str} -- path to input file
            output_file {str} -- path to output file
        """

        audio = AudioSegment.from_ogg(input_file)
        audio.export(output_file, format="mp3")
