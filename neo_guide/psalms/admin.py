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
    list_display = (
        'name',
        'page_number',
        'card_color',
        'image_number',
        'audio_number',
        'is_valid',
        'active',
        'created_at',
        'updated_at',
    )
    search_fields = ('name', 'page_number')
    list_filter = ('card_color', 'active')
    inlines = [PsalmImageInline, PsalmAudioInline]

    def is_valid(self, obj):
        default_image = obj.psalm_image.filter(default=True)

        if default_image.count() > 1 or not default_image:
            return False

        return True

    def image_number(self, obj):
        return obj.psalm_image.filter(active=True).count()

    def audio_number(self, obj):
        return obj.psalm_audio.filter(active=True).count()

    is_valid.boolean = True
