from rest_framework import serializers
from .models import Exposant, ReservationStand


class ExposantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exposant
        fields = "__all__"


class ReservationStandSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReservationStand
        fields = ["nom_entreprise", "email", "telephone", "pays", "categorie_souhaitee", "message"]