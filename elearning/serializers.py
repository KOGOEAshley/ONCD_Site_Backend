from rest_framework import serializers
from .models import ModuleELearning, InscriptionModule


class ModuleELearningSerializer(serializers.ModelSerializer):
    nombre_inscrits = serializers.SerializerMethodField()

    class Meta:
        model = ModuleELearning
        fields = ["id", "titre", "duree", "niveau", "description", "lien_video", "nombre_inscrits"]

    def get_nombre_inscrits(self, obj):
        return obj.inscriptions.count()


class InscriptionModuleSerializer(serializers.ModelSerializer):
    module = ModuleELearningSerializer(read_only=True)

    class Meta:
        model = InscriptionModule
        fields = ["id", "module", "date_inscription", "termine", "date_completion"]
        