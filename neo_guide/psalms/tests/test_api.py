import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from neo_guide.psalms.models import Psalm
from neo_guide.psalms.models import PsalmAudio
from neo_guide.psalms.models import PsalmImage
from neo_guide.psalms.tests.factories import PsalmAudioFactory
from neo_guide.psalms.tests.factories import PsalmFactory
from neo_guide.psalms.tests.factories import PsalmImageFactory


@pytest.mark.django_db
class TestPsalmListView:
    def test_get_psalms_when_no_audio_and_no_images(self, api_client):
        PsalmFactory.create_batch(3)
        response = api_client.get(reverse('v1-psalms:psalm-list'))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == Psalm.objects.count()

    def test_get_psalms_with_images(self, api_client):
        psalm = PsalmFactory()
        PsalmImageFactory(psalm=psalm)

        response = api_client.get(reverse('v1-psalms:psalm-list'))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == Psalm.objects.count()
        assert len(response.data['results'][0]['images']) == PsalmImage.objects.count()

    def test_get_psalms_with_audios(self, api_client):
        psalm = PsalmFactory()
        PsalmAudioFactory(psalm=psalm)

        response = api_client.get(reverse('v1-psalms:psalm-list'))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == Psalm.objects.count()
        assert len(response.data['results'][0]['recordings']) == PsalmAudio.objects.count()


@pytest.mark.django_db
class TestPsalmDetailsView:
    def test_get_psalm_details(self, api_client):
        psalm = PsalmFactory()

        response = api_client.get(reverse('v1-psalms:psalm-detail', args=(psalm.id,)))

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == psalm.name

    def test_get_psalm_details_not_found(self, api_client):
        response = api_client.get(reverse('v1-psalms:psalm-detail', args=(100,)))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_psalm_default_image(self, api_client):
        psalm = PsalmFactory()
        PsalmImageFactory(psalm=psalm, default=True)

        response = api_client.get(reverse('v1-psalms:psalm-detail', args=(psalm.id,)))

        assert response.status_code == status.HTTP_200_OK
        assert response.data['default_image'] is not None

    def test_get_psalm_without_default_image(self, api_client):
        psalm = PsalmFactory()
        PsalmImageFactory(psalm=psalm)

        response = api_client.get(reverse('v1-psalms:psalm-detail', args=(psalm.id,)))

        assert response.status_code == status.HTTP_200_OK
        assert response.data['default_image'] is None

    def test_get_psalm_details_with_images(self, api_client):
        psalm = PsalmFactory()
        PsalmImageFactory.create_batch(5, psalm=psalm)

        response = api_client.get(reverse('v1-psalms:psalm-detail', args=(psalm.id,)))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['images']) == PsalmImage.objects.count()

    def test_get_psalm_details_without_images(self, api_client):
        psalm = PsalmFactory()

        response = api_client.get(reverse('v1-psalms:psalm-detail', args=(psalm.id,)))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['images']) == PsalmImage.objects.count()

    def test_get_psalm_details_with_recordings(self, api_client):
        psalm = PsalmFactory()
        PsalmAudioFactory.create_batch(5, psalm=psalm)

        response = api_client.get(reverse('v1-psalms:psalm-detail', args=(psalm.id,)))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['recordings']) == PsalmAudio.objects.count()

    def test_get_psalm_details_without_recordings(self, api_client):
        psalm = PsalmFactory()

        response = api_client.get(reverse('v1-psalms:psalm-detail', args=(psalm.id,)))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['recordings']) == PsalmAudio.objects.count()
