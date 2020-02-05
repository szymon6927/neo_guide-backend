from django.contrib import admin
from django.utils.html import mark_safe

from neo_guide.psalms.models import Psalm
from neo_guide.psalms.models import PsalmAudio
from neo_guide.psalms.models import PsalmImage


class PsalmImageInline(admin.TabularInline):
    model = PsalmImage
    extra = 1
    readonly_fields = ('psalm_image',)

    def psalm_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="{obj.image.width // 2}" height={obj.image.height // 2} />')


class PsalmAudioInline(admin.TabularInline):
    model = PsalmAudio
    extra = 1
    readonly_fields = ('psalm_audio',)

    def psalm_audio(self, obj):
        return mark_safe(
            f'<audio controls autobuffer style="width:500px;"><source src="{obj.audio.url}" type="audio/mp3"></audio>'
        )


@admin.register(Psalm)
class PsalmAdmin(admin.ModelAdmin):
    list_display = ('name', 'page_number', 'card_color', 'active', 'created_at', 'updated_at')
    search_fields = ('name', 'page_number')
    list_filter = ('card_color', 'active')
    inlines = [PsalmImageInline, PsalmAudioInline]
