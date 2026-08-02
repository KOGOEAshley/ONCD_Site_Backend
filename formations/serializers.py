from rest_framework import serializers
from .models import Formation, Participation


class FormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formation
        fields = ["id", "nom", "date_debut", "date_fin", "heures", "lieu"]


class ParticipationSerializer(serializers.ModelSerializer):
    formation = FormationSerializer(read_only=True)

    class Meta:
        model = Participation
        fields = ["id", "formation", "heures_obtenues", "valide"]