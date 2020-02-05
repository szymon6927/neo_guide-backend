from django.db import models
from django.utils.translation import gettext as _

from neo_guide.core.models import CreatedAtUpdatedAtModel
from neo_guide.psalms.choices import CardColorChoices
from neo_guide.psalms.utils import psalm_audio_directory_path
from neo_guide.psalms.utils import psalm_image_directory_path
from neo_guide.psalms.validators import audio_validator
from neo_guide.psalms.validators import image_validator
from neo_guide.psalms.validators import page_number_validator


class Psalm(CreatedAtUpdatedAtModel):
    name = models.CharField(_('Tytuł Pieśni'), max_length=200, unique=True)
    page_number = models.PositiveIntegerField(_('Numer strony'), unique=True, validators=page_number_validator)
    card_color = models.CharField(
        _('Kolor kartki'), choices=CardColorChoices.choices, default=CardColorChoices.WHITE.value, max_length=20
    )
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Psalm')
        verbose_name_plural = _('Psalmy')
        ordering = ['page_number']

    def __str__(self):
        return self.name


class PsalmImage(CreatedAtUpdatedAtModel):
    image = models.ImageField(
        _('Zdjęcie pieśni'), upload_to=psalm_image_directory_path, validators=image_validator, blank=True
    )
    active = models.BooleanField(_('Aktywny'), default=True)
    default = models.BooleanField(_('Domyślny'), default=False)
    psalm = models.ForeignKey(Psalm, related_name='psalm_image', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Zdjęcie psalmu')
        verbose_name_plural = _('Zdjęcia psalmów')
        ordering = ['psalm__page_number']

    def __str__(self):
        return _(f'Zdjęcie dla {self.psalm.name}')


class PsalmAudio(CreatedAtUpdatedAtModel):
    audio = models.FileField(
        _('Nagranie audio'),
        upload_to=psalm_audio_directory_path,
        help_text=_('.mp3, .wav, .wma lub flac'),
        validators=audio_validator,
        blank=True,
    )
    active = models.BooleanField(_('Aktywny'), default=True)
    psalm = models.ForeignKey(Psalm, related_name='psalm_audio', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Nagranie psalmu')
        verbose_name_plural = _('Nagrania psalmów')
        ordering = ['psalm__page_number']

    def __str__(self):
        return _(f'Nagranie dla {self.psalm.name}')
