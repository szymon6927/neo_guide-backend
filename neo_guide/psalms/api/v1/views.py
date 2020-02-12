from django.db.models import OuterRef
from django.db.models import Prefetch
from django.db.models import Subquery
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from neo_guide.psalms.api.v1.serializers import PsalmSerializer
from neo_guide.psalms.models import Psalm
from neo_guide.psalms.models import PsalmAudio
from neo_guide.psalms.models import PsalmImage


class PsalmViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ('card_color',)
    search_fields = ('name', 'page_number')
    ordering_fields = ('name', 'page_number')
    serializer_class = PsalmSerializer
    queryset = (
        Psalm.objects.prefetch_related(
            Prefetch('psalm_audio', queryset=PsalmAudio.objects.filter(active=True)),
            Prefetch('psalm_image', queryset=PsalmImage.objects.filter(active=True, default=False)),
        )
        .annotate(
            default_image=Subquery(
                PsalmImage.objects.filter(active=True, default=True, psalm=OuterRef('id')).values('image')[:1]
            )
        )
        .filter(active=True)
        .order_by('page_number')
    )
