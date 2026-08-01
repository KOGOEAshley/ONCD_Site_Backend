import io

from django.http import HttpResponse
from django.utils import timezone
from rest_framework import viewsets, filters, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from documents.models import ModeleDocument
from documents.services import rendre_modele, generer_pdf_depuis_html

from .models import Praticien
from .serializers import PraticienSerializer, InscriptionSerializer


class PraticienViewSet(viewsets.ModelViewSet):
    queryset = Praticien.objects.all()
    serializer_class = PraticienSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["nom", "prenom", "ville", "specialite"]


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "username": user.username,
        })


class InscriptionView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        serializer = InscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        praticien = serializer.save()

        token, _ = Token.objects.get_or_create(user=praticien.user)

        return Response(
            {
                "message": "Votre demande d'inscription a été envoyée. Elle est en attente de validation par l'Ordre.",
                "token": token.key,
                "praticien": PraticienSerializer(praticien).data,
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["GET", "PATCH"])
@parser_classes([MultiPartParser, FormParser, JSONParser])
@permission_classes([IsAuthenticated])
def mon_profil(request):
    try:
        praticien = request.user.praticien
    except Praticien.DoesNotExist:
        return Response({"detail": "Aucun profil praticien lié à ce compte."}, status=404)

    if request.method == "PATCH":
        photo = request.FILES.get("photo")
        if photo:
            praticien.photo = photo
            praticien.save()

    return Response(PraticienSerializer(praticien).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def mon_attestation(request):
    """
    GET /api/mon-attestation/  (nécessite le header Authorization: Token xxxx)
    Génère un PDF à partir du modèle "attestation_inscription" stocké en base.
    """
    try:
        praticien = request.user.praticien
    except Praticien.DoesNotExist:
        return Response({"detail": "Aucun profil praticien lié à ce compte."}, status=404)

    if praticien.statut != "actif":
        return Response(
            {"detail": "Votre dossier n'est pas encore validé : l'attestation n'est pas disponible."},
            status=403,
        )

    try:
        modele = ModeleDocument.objects.get(code="attestation_inscription", actif=True)
    except ModeleDocument.DoesNotExist:
        return Response(
            {"detail": "Le modèle 'attestation_inscription' n'existe pas encore. Créez-le dans l'admin."},
            status=500,
        )

    html = rendre_modele(modele, {"praticien": praticien, "date_edition": timezone.now().date()})

    try:
        pdf_bytes = generer_pdf_depuis_html(html)
    except ValueError:
        return Response({"detail": "Erreur lors de la génération du PDF."}, status=500)

    reponse = HttpResponse(pdf_bytes, content_type="application/pdf")
    reponse["Content-Disposition"] = f'attachment; filename="attestation_{praticien.numero_inscription}.pdf"'
    return reponse