from rest_framework import serializers
from .models import MembreConseil


class MembreConseilSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembreConseil
        fields = "__all__"