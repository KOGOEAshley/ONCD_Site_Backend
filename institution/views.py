from rest_framework import viewsets
from .models import MembreConseil
from .serializers import MembreConseilSerializer


class MembreConseilViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MembreConseil.objects.all()
    serializer_class = MembreConseilSerializer