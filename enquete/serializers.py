from rest_framework import serializers
from .models import FicheCollecteDonnees


class FicheCollecteDonneesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FicheCollecteDonnees
        exclude = ["date_soumission"]