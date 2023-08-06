# Text to Audio SDK

[![PyPI Version][pypi-image]][pypi-url]
[![Build Status][build-image]][build-url]
[![Code Coverage][coverage-image]][coverage-url]
[![Code Quality][quality-image]][quality-url]
[![License][license-image]][license-url]

The Yandex Text to Audio SDK is a Python package that allows you to convert text to audio using Yandex premium voices. It provides an easy-to-use asynchronous interface for generating audio files from text with customizable voice, speed, and other parameters.

## Installation

You can install the SDK from PyPI using pip:

```bash
pip install txt2voice
```

## Quick Start

Here's a simple example demonstrating how to use the SDK to convert text to audio:

```python
import asyncio

from txt2voice.api import TextToVoice, RequestParams
from txt2voice.models import VoiceParams, SpeedParams, AudioContent


async def main():
    token = 'YOUR_IAM_TOKEN'
    folder_id = 'YOUR_FOLDER_ID'
    text = 'Hello, this is an example text for audio conversion!'
    output_file = 'output_audio.mp3'

    api = TextToVoice(url='https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize')

    convert_params = RequestParams(
        voice=VoiceParams(male='fillip', female='alyona'),
        speed=SpeedParams(speed=1.0),
        path_to_audiofiles=output_file,
        folder_id=folder_id,
        iam_token=token,
        lang='ru-RU',
        text=text
    )

    audio_content: AudioContent = await api.request_audio_content(convert_params)
    api.convert_ogg_to_mp3(audio_content, 'output_audio.mp3')


if __name__ == '__main__':
    asyncio.run(main())
```

## Dependencies

The Yandex Text to Audio SDK has the following dependencies:

- aiohttp
- pydantic
- pydub

You can install them using pip with the following command:

```bash
pip install aiohttp pydantic pydub
```

## Contributing

Contributions to the project are welcome! If you find a bug, have a feature request, or want to contribute code, please open an issue or submit a pull request.

## License

This SDK is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Happy audio conversion with Yandex Text to Audio SDK!

<!-- Badges -->

[pypi-image]: https://img.shields.io/pypi/v/txt2voice
[pypi-url]: https://pypi.org/project/txt2voice/
[build-image]: https://github.com/zemags/python-yandex-speech-kit/actions/workflows/build.yml/badge.svg
[build-url]: https://github.com/zemags/python-yandex-speech-kit/actions/workflows/build.yml
[coverage-image]: https://codecov.io/gh/zemags/python-yandex-speech-kit/branch/main/graph/badge.svg
[coverage-url]: https://codecov.io/gh/zemags/python-yandex-speech-kit
[quality-image]: https://api.codeclimate.com/v1/badges/d36533b74a159ebe78b1/maintainability
[quality-url]: https://codeclimate.com/github/zemags/python-yandex-speech-kit
[license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[license-url]: https://opensource.org/licenses/MIT