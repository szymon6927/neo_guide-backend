from rest_framework.serializers import ModelSerializer

from neo_guide.psalms.models import Psalm
from neo_guide.psalms.models import PsalmAudio
from neo_guide.psalms.models import PsalmImage


class PsalmImageSerializer(ModelSerializer):
    class Meta:
        model = PsalmImage
        fields = ('image',)


class PsalmAudioSerializer(ModelSerializer):
    class Meta:
        model = PsalmAudio
        fields = ('audio',)


class PsalmSerializer(ModelSerializer):
    recordings = PsalmAudioSerializer(source='psalm_audio', many=True, read_only=True)
    images = PsalmImageSerializer(source='psalm_image', many=True, read_only=True)

    class Meta:
        model = Psalm
        fields = ['name', 'page_number', 'card_color', 'recordings', 'images']
