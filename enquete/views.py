from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import FicheCollecteDonneesSerializer


class SoumettreFicheView(APIView):
    """
    POST /api/soumettre-fiche-enquete/
    Formulaire public — aucune connexion requise, ouvert à tous les dentistes.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = FicheCollecteDonneesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Merci, votre fiche a bien été enregistrée."},
            status=status.HTTP_201_CREATED,
        )