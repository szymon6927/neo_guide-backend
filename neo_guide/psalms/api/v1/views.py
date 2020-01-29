from rest_framework.viewsets import ModelViewSet

from neo_guide.psalms.api.v1.serializers import PsalmSerializer
from neo_guide.psalms.models import Psalm


class PsalmViewSet(ModelViewSet):
    filterset_fields = ('name',)
    ordering_fields = ('name', 'card_number')
    serializer_class = PsalmSerializer
    queryset = Psalm.objects.all()
