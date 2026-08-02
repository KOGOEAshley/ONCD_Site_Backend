from rest_framework import viewsets, filters
from .models import Evenement
from .serializers import EvenementSerializer


class EvenementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Evenement.objects.all()
    serializer_class = EvenementSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["titre", "lieu", "tags"]