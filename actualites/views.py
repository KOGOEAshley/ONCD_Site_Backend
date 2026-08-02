from rest_framework import viewsets, filters
from .models import Actualite
from .serializers import ActualiteSerializer


class ActualiteViewSet(viewsets.ReadOnlyModelViewSet):
    """Lecture publique uniquement — la publication se fait via l'admin."""

    queryset = Actualite.objects.all()
    serializer_class = ActualiteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["titre", "extrait", "categorie"]