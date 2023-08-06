import os
from asyncio import streams
from http import HTTPStatus
from unittest.mock import Mock

import pytest
from asynctest import patch, CoroutineMock
from pydub import AudioSegment

from txt2voice.api import TextToVoice
from txt2voice.models import RequestParams, VoiceParams, SpeedParams, AudioContent


def mock_streamreader_object() -> streams.StreamReader:
    data: bytes = b"audio_chunk"
    stream = streams.StreamReader(limit=2)
    stream.feed_data(data)
    stream.feed_eof()
    return stream


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.post")
async def test_request_audio_content(mocked_client_session):
    mock_response = Mock()
    mock_response.status = HTTPStatus.OK
    mock_response.content = mock_streamreader_object()

    mocked_client_session().__aenter__ = CoroutineMock(return_value=mock_response)

    api = TextToVoice(url='fake-url')
    request_params = RequestParams(
        voice=VoiceParams(male='filipp', female='alyona'),
        speed=SpeedParams(speed=1.0),
        path_to_audiofiles='fake-file.ogg',
        folder_id='fake-folder-id',
        iam_token='fake-iam-token',
        lang='ru-RU',
        text='hello'
    )

    result = await api.request_audio_content(params=request_params)
    assert result.content == b"audio_chunk"
    assert mocked_client_session.call_count == 2


@pytest.mark.asyncio
@patch("aiohttp.ClientSession.post")
async def test_request_audio_content_with_error(mocked_client_session):
    mock_response = Mock()
    mock_response.status = HTTPStatus.BAD_REQUEST
    mock_response.content = mock_streamreader_object()

    mocked_client_session().__aenter__ = CoroutineMock(return_value=mock_response)

    api = TextToVoice(url='fake-url')
    request_params = RequestParams(
        voice=VoiceParams(male='filipp', female='alyona'),
        speed=SpeedParams(speed=1.0),
        path_to_audiofiles='fake-file.ogg',
        folder_id='fake-folder-id',
        iam_token='fake-iam-token',
        lang='ru-RU',
        text='привет'
    )
    # catch error
    with pytest.raises(Exception):
        await api.request_audio_content(params=request_params)

    assert mocked_client_session.call_count == 2


@pytest.mark.asyncio
async def test_save_audio_to_file():
    request_params = RequestParams(
        voice=VoiceParams(male='filipp', female='alyona'),
        speed=SpeedParams(speed=1.0),
        path_to_audiofiles='fake-file.ogg',
        folder_id='fake-folder-id',
        iam_token='fake-iam-token',
        lang='ru-RU',
        text='привет'
    )

    with patch("txt2voice.api.TextToVoice.request_audio_content", return_value=AudioContent(content=b'audio_chunk')) as p:
        await TextToVoice(url='fake-url').save_audio_to_file(request_params)
        assert p.call_count == 1
        assert os.path.exists('fake-file.ogg')
        os.remove('fake-file.ogg')


def test_convert_ogg_to_mp3(mocker):
    input_file = "fake-file.ogg"
    output_file = "fake-file.mp3"

    mock_from_ogg = mocker.patch('pydub.AudioSegment.from_ogg', autospec=True)
    mock_audio = Mock(spec=AudioSegment)
    mock_from_ogg.return_value = mock_audio

    mock_export = mock_audio.export
    mock_export.return_value = "mock_export_result"

    your_instance = TextToVoice(url='fake-url')
    your_instance.convert_ogg_to_mp3(input_file, output_file)
    mock_from_ogg.assert_called_once_with(input_file)
    mock_export.assert_called_once_with(output_file, format="mp3")
