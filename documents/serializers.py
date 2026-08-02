from rest_framework import serializers
from .models import DocumentTelechargeable


class DocumentTelechargeableSerializer(serializers.ModelSerializer):
    type_fichier = serializers.ReadOnlyField()
    taille_affichee = serializers.ReadOnlyField()

    class Meta:
        model = DocumentTelechargeable
        fields = ["id", "titre", "categorie", "fichier", "date_maj", "type_fichier", "taille_affichee"]