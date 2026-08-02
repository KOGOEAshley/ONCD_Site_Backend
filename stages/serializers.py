from rest_framework import serializers
from .models import Stage, CandidatureStage


class StageSerializer(serializers.ModelSerializer):
    places_restantes = serializers.ReadOnlyField()

    class Meta:
        model = Stage
        fields = "__all__"


class CandidatureStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidatureStage
        fields = ["stage", "nom", "prenom", "email", "telephone", "niveau_actuel", "cv", "message"]