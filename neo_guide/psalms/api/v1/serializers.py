from django.conf import settings
from rest_framework import serializers

from neo_guide.psalms.models import Psalm
from neo_guide.psalms.models import PsalmAudio
from neo_guide.psalms.models import PsalmImage


class PsalmImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PsalmImage
        fields = ('image', 'active', 'default')


class PsalmAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PsalmAudio
        fields = ('audio', 'active')


class PsalmSerializer(serializers.ModelSerializer):
    recordings = PsalmAudioSerializer(source='psalm_audio', many=True, read_only=True)
    images = PsalmImageSerializer(source='psalm_image', many=True, read_only=True)
    default_image = serializers.SerializerMethodField()

    def get_default_image(self, psalm):
        if psalm.default_image:
            default_image_url = f'{settings.MEDIA_URL}{psalm.default_image}'
            return self.context['request'].build_absolute_uri(default_image_url)

        return None

    class Meta:
        model = Psalm
        fields = ('id', 'name', 'page_number', 'card_color', 'recordings', 'images', 'default_image')
