from django.utils import timezone
from rest_framework import viewsets, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from praticiens.models import Praticien
from .models import ModuleELearning, InscriptionModule
from .serializers import ModuleELearningSerializer, InscriptionModuleSerializer


class ModuleELearningViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ModuleELearning.objects.all()
    serializer_class = ModuleELearningSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["titre"]

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def inscrire(self, request, pk=None):
        module = self.get_object()
        try:
            praticien = request.user.praticien
        except Praticien.DoesNotExist:
            return Response({"detail": "Aucun profil praticien lié à ce compte."}, status=404)

        inscription, cree = InscriptionModule.objects.get_or_create(praticien=praticien, module=module)
        message = "Inscription enregistrée." if cree else "Vous êtes déjà inscrit à ce module."
        return Response({"message": message, "inscription": InscriptionModuleSerializer(inscription).data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def mes_modules(request):
    try:
        praticien = request.user.praticien
    except Praticien.DoesNotExist:
        return Response({"detail": "Aucun profil praticien lié à ce compte."}, status=404)

    inscriptions = InscriptionModule.objects.filter(praticien=praticien).select_related("module")
    return Response(InscriptionModuleSerializer(inscriptions, many=True).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def terminer_module(request, inscription_id):
    try:
        praticien = request.user.praticien
    except Praticien.DoesNotExist:
        return Response({"detail": "Aucun profil praticien lié à ce compte."}, status=404)

    try:
        inscription = InscriptionModule.objects.get(id=inscription_id, praticien=praticien)
    except InscriptionModule.DoesNotExist:
        return Response({"detail": "Inscription introuvable."}, status=404)

    inscription.termine = True
    inscription.date_completion = timezone.now()
    inscription.save()
    return Response(InscriptionModuleSerializer(inscription).data)