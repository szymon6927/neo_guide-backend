from django.contrib import admin
from django.db.models import Case
from django.db.models import Count
from django.db.models import IntegerField
from django.db.models import Q
from django.db.models import Value
from django.db.models import When
from django.utils.html import mark_safe

from neo_guide.psalms.admin_filters import PsalmLiturgicalPeriodAdminFilter
from neo_guide.psalms.admin_filters import PsalmNeoStageAdminFilter
from neo_guide.psalms.admin_filters import PsalmTypeAdminFilter
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
    list_filter = (
        'card_color',
        PsalmTypeAdminFilter,
        PsalmLiturgicalPeriodAdminFilter,
        PsalmNeoStageAdminFilter,
        'active',
    )
    inlines = [PsalmImageInline, PsalmAudioInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            image_number=Count('psalm_image', distinct=True),
            default_images=Count('psalm_image', distinct=True, filter=Q(psalm_image__default=True)),
            audio_number=Count('psalm_audio', distinct=True),
            is_valid=Case(
                When(default_images__gt=1, then=Value(0)),
                When(default_images__exact=0, then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            ),
        )

        return queryset

    def is_valid(self, obj):
        return obj.is_valid

    def image_number(self, obj):
        return obj.image_number

    def audio_number(self, obj):
        return obj.audio_number

    is_valid.boolean = True
    image_number.admin_order_field = 'image_number'
    audio_number.admin_order_field = 'audio_number'
    is_valid.admin_order_field = 'is_valid'
