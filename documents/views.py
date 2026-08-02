from rest_framework import viewsets, filters
from .models import DocumentTelechargeable
from .serializers import DocumentTelechargeableSerializer


class DocumentTelechargeableViewSet(viewsets.ReadOnlyModelViewSet):
    """Bibliothèque publique de documents téléchargeables."""

    queryset = DocumentTelechargeable.objects.all()
    serializer_class = DocumentTelechargeableSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["titre"]