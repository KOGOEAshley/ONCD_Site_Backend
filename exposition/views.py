from rest_framework import viewsets, filters, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Exposant, ReservationStand
from .serializers import ExposantSerializer, ReservationStandSerializer


class ExposantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Exposant.objects.all()
    serializer_class = ExposantSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["nom", "pays", "produits"]


class ReserverStandView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ReservationStandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Votre demande de réservation a été envoyée. L'Ordre vous contactera prochainement."},
            status=status.HTTP_201_CREATED,
        )