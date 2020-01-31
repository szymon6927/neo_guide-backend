import tempfile

import pytest
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from neo_guide.psalms.tests.factories import PsalmAudioFactory
from neo_guide.psalms.tests.factories import PsalmFactory
from neo_guide.psalms.tests.factories import PsalmImageFactory


@pytest.fixture
def temp_wrong_image():
    tmp = tempfile.NamedTemporaryFile(delete=True, suffix='.psd', dir=settings.MEDIA_ROOT)
    try:
        yield tmp.name
    finally:
        tmp.close()


@pytest.fixture
def temp_wrong_audio():
    tmp = tempfile.NamedTemporaryFile(delete=True, suffix='.ogg', dir=settings.MEDIA_ROOT)
    try:
        yield tmp.name
    finally:
        tmp.close()


class TestPsalmModel:
    @pytest.mark.django_db
    def test_unique_psalm_name(self):
        psalm_name = 'test_name'

        with pytest.raises(IntegrityError):
            PsalmFactory.create_batch(2, name=psalm_name)

    @pytest.mark.django_db
    def test_psalm_page_number_range_too_large(self):
        psalm = PsalmFactory(page_number=1000)

        with pytest.raises(ValidationError):
            psalm.full_clean()

    @pytest.mark.django_db
    def test_psalm_page_number_range_too_small(self):
        psalm = PsalmFactory(page_number=0)

        with pytest.raises(ValidationError):
            psalm.full_clean()


class TestPsalmImageModel:
    @pytest.mark.django_db
    def test_psalm_image_wrong_file_extension(self, temp_wrong_image):
        psalm_image = PsalmImageFactory(image=temp_wrong_image)

        with pytest.raises(ValidationError):
            psalm_image.full_clean()


class TestPsalmAudioModel:
    @pytest.mark.django_db
    def test_psalm_audio_wrong_file_extension(self, temp_wrong_audio):
        psalm_audio = PsalmAudioFactory(audio=temp_wrong_audio)

        with pytest.raises(ValidationError):
            psalm_audio.full_clean()
