from rest_framework import serializers
from .models import Cotisation, BaremeCotisation


class BaremeCotisationSerializer(serializers.ModelSerializer):
    secteur_display = serializers.CharField(source="get_secteur_display", read_only=True)

    class Meta:
        model = BaremeCotisation
        fields = ["id", "secteur", "secteur_display", "montant"]


class CotisationSerializer(serializers.ModelSerializer):
    statut_display = serializers.CharField(source="get_statut_display", read_only=True)

    class Meta:
        model = Cotisation
        fields = ["id", "annee", "montant", "date_echeance", "statut", "statut_display", "date_paiement", "methode_paiement"]