from django.http import HttpResponse
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from documents.models import ModeleDocument
from documents.services import rendre_modele, generer_pdf_depuis_html
from praticiens.models import Praticien

from .models import Participation
from .serializers import ParticipationSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def mes_formations(request):
    try:
        praticien = request.user.praticien
    except Praticien.DoesNotExist:
        return Response({"detail": "Aucun profil praticien lié à ce compte."}, status=404)

    participations = (
        Participation.objects.filter(praticien=praticien, valide=True)
        .select_related("formation")
        .order_by("-formation__date_debut")
    )
    return Response(ParticipationSerializer(participations, many=True).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def mon_attestation_formation(request, participation_id):
    try:
        praticien = request.user.praticien
    except Praticien.DoesNotExist:
        return Response({"detail": "Aucun profil praticien lié à ce compte."}, status=404)

    try:
        participation = Participation.objects.select_related("formation", "praticien").get(id=participation_id)
    except Participation.DoesNotExist:
        return Response({"detail": "Participation introuvable."}, status=404)

    if participation.praticien_id != praticien.id:
        return Response({"detail": "Vous n'êtes pas autorisé à télécharger ce document."}, status=403)

    try:
        modele = ModeleDocument.objects.get(code="attestation_formation", actif=True)
    except ModeleDocument.DoesNotExist:
        return Response({"detail": "Modèle 'attestation_formation' introuvable."}, status=500)

    html = rendre_modele(modele, {
        "praticien": participation.praticien,
        "participation": participation,
        "date_edition": timezone.now().date(),
    })

    try:
        pdf_bytes = generer_pdf_depuis_html(html)
    except ValueError:
        return Response({"detail": "Erreur lors de la génération du PDF."}, status=500)

    nom_fichier = f"attestation_{participation.formation.nom}.pdf".replace(" ", "_")
    reponse = HttpResponse(pdf_bytes, content_type="application/pdf")
    reponse["Content-Disposition"] = f'attachment; filename="{nom_fichier}"'
    return reponse