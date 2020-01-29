from django.db import models
from django.utils.translation import gettext as _

from neo_guide.psalms.choices import CardColorChoices
from neo_guide.psalms.utils import psalm_audio_directory_path
from neo_guide.psalms.utils import psalm_image_directory_path


class Psalm(models.Model):
    name = models.CharField(_('Tytuł Pieśni'), max_length=200)
    page_number = models.IntegerField(_('Numer strony'))
    card_color = models.CharField(
        _('Kolor kartki'), choices=CardColorChoices.choices, default=CardColorChoices.WHITE.value, max_length=20
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class PsalmImage(models.Model):
    image = models.ImageField(_('Zdjęcie pieśni'), upload_to=psalm_image_directory_path)
    active = models.BooleanField(_('Aktywny'))
    psalm = models.ForeignKey(Psalm, related_name='psalm_image', on_delete=models.CASCADE)

    def __str__(self):
        return self.psalm.name


class PsalmAudio(models.Model):
    audio = models.FileField(_('Nagranie audio'), upload_to=psalm_audio_directory_path)
    active = models.BooleanField(_('Aktywny'))
    psalm = models.ForeignKey(Psalm, related_name='psalm_audio', on_delete=models.CASCADE)

    def __str__(self):
        return self.psalm.name
