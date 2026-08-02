from rest_framework import serializers
from .models import Evenement


class EvenementSerializer(serializers.ModelSerializer):
    places_restantes = serializers.ReadOnlyField()

    class Meta:
        model = Evenement
        fields = "__all__"