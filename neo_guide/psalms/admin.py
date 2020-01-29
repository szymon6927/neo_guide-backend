from django.contrib import admin

from neo_guide.psalms.models import Psalm
from neo_guide.psalms.models import PsalmAudio
from neo_guide.psalms.models import PsalmImage


class PsalmImageInline(admin.TabularInline):
    model = PsalmImage
    extra = 1


class PsalmAudioInline(admin.TabularInline):
    model = PsalmAudio
    extra = 1


@admin.register(Psalm)
class PsalmAdmin(admin.ModelAdmin):
    list_display = ('name', 'page_number', 'card_color')
    inlines = [PsalmImageInline, PsalmAudioInline]
