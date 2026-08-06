from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from praticiens.models import Praticien
from .models import Cotisation, BaremeCotisation
from .serializers import CotisationSerializer, BaremeCotisationSerializer


class BaremeCotisationViewSet(viewsets.ReadOnlyModelViewSet):
    """Barème public des cotisations — lecture seule, modifiable uniquement via l'admin."""

    queryset = BaremeCotisation.objects.all()
    serializer_class = BaremeCotisationSerializer
    permission_classes = [AllowAny]


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def ma_cotisation(request):
    """
    GET /api/ma-cotisation/
    Renvoie la cotisation de l'année en cours pour le praticien connecté.
    Si elle n'a pas encore été générée par le secrétariat, renvoie
    "generee": false plutôt qu'une erreur, pour un affichage propre côté frontend.
    """
    try:
        praticien = request.user.praticien
    except Praticien.DoesNotExist:
        return Response({"detail": "Aucun profil praticien lié à ce compte."}, status=404)

    annee = timezone.now().year
    cotisation = Cotisation.objects.filter(praticien=praticien, annee=annee).first()

    if not cotisation:
        return Response({"generee": False, "annee": annee})

    donnees = CotisationSerializer(cotisation).data
    donnees["generee"] = True
    return Response(donnees)