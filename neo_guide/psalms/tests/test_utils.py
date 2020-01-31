import pytest

from neo_guide.psalms.tests.factories import PsalmAudioFactory
from neo_guide.psalms.tests.factories import PsalmImageFactory
from neo_guide.psalms.utils import psalm_audio_directory_path
from neo_guide.psalms.utils import psalm_image_directory_path


@pytest.mark.django_db
def test_psalm_image_directory_path():
    file_name = 'test_name'
    psalm_image = PsalmImageFactory()

    dir_path = psalm_image_directory_path(psalm_image, file_name)

    assert str(psalm_image.psalm.id) in dir_path
    assert file_name in dir_path


@pytest.mark.django_db
def test_psalm_audio_directory_path():
    file_name = 'test_name'
    psalm_audio = PsalmAudioFactory()

    dir_path = psalm_audio_directory_path(psalm_audio, file_name)

    assert str(psalm_audio.psalm.id) in dir_path
    assert file_name in dir_path
