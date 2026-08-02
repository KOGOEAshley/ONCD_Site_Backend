from rest_framework import viewsets, filters, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response

from .models import Stage, CandidatureStage
from .serializers import StageSerializer, CandidatureStageSerializer


class StageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["etablissement", "ville", "specialite"]


class PostulerStageView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        serializer = CandidatureStageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Votre candidature a été envoyée. L'établissement vous contactera directement."},
            status=status.HTTP_201_CREATED,
        )