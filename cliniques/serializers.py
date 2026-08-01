from rest_framework import serializers
from .models import Clinique
from praticiens.serializers import PraticienSerializer


class CliniqueSerializer(serializers.ModelSerializer):
    # Affiche les praticiens en détail plutôt que juste leurs ID
    praticiens = PraticienSerializer(many=True, read_only=True)

    class Meta:
        model = Clinique
        fields = "__all__"