from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator


def validate_audio_file_size(value):
    limit = settings.MAX_AUDIO_UPLOAD_SIZE

    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 10MB.')


def validate_image_file_size(value):
    limit = settings.MAX_IMAGE_UPLOAD_SIZE

    if value.size > limit:
        raise ValidationError('Image too large. Size should not exceed 3MB.')


page_number_validator = [MinValueValidator(1), MaxValueValidator(500)]
audio_validator = [FileExtensionValidator(['mp3', 'wav', 'wma', 'flac']), validate_audio_file_size]
image_validator = [validate_image_file_size]
