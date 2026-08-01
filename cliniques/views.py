from rest_framework import viewsets
from .models import Clinique
from .serializers import CliniqueSerializer


class CliniqueViewSet(viewsets.ModelViewSet):
    queryset = Clinique.objects.all()
    serializer_class = CliniqueSerializer