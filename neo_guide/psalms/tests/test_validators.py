from dataclasses import dataclass

import pytest
from django.core.exceptions import ValidationError

from neo_guide.psalms.validators import validate_audio_file_size
from neo_guide.psalms.validators import validate_image_file_size


@dataclass
class FakeValue:
    size: int


def test_validate_image_file_size_when_size_too_large():
    value = FakeValue(4 * 1024 * 1024)

    with pytest.raises(ValidationError):
        validate_image_file_size(value)


def test_validate_audio_file_size_when_size_too_large():
    value = FakeValue(11 * 1024 * 1024)

    with pytest.raises(ValidationError):
        validate_audio_file_size(value)
