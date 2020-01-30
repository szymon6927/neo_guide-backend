from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from neo_guide.psalms.api.v1.serializers import PsalmSerializer
from neo_guide.psalms.models import Psalm


class PsalmViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ('card_color',)
    search_fields = ('^name',)
    ordering_fields = ('name', 'card_number')
    serializer_class = PsalmSerializer
    queryset = (
        Psalm.objects.filter(
            (
                Q(active=True)
                & (Q(psalm_audio__active=True) | Q(psalm_image__default=True) | Q(psalm_audio__active=True))
            )
        )
        .order_by('page_number')
        .distinct()
    )
