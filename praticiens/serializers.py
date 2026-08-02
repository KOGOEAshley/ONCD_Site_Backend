from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from .models import Praticien


class PraticienSerializer(serializers.ModelSerializer):
    class Meta:
        model = Praticien
        fields = "__all__"


class InscriptionSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=6)

    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    telephone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    ville = serializers.CharField(max_length=100)
    region = serializers.CharField(max_length=100)
    specialite = serializers.CharField(max_length=150)
    secteur = serializers.ChoiceField(
    choices=Praticien.SECTEUR_CHOICES,
    error_messages={"required": "Veuillez indiquer votre secteur d'exercice."},
)
    diplome = serializers.FileField(
    required=True,
    error_messages={
        "required": "Le diplôme ou CV est obligatoire pour soumettre votre dossier.",
        "invalid": "Fichier invalide. Formats acceptés : PDF, JPG, PNG.",
    },
)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur est déjà utilisé.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Un compte existe déjà avec cet email.")
        return value

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(
                username=validated_data["username"],
                email=validated_data["email"],
                password=validated_data["password"],
            )
            praticien = Praticien.objects.create(
                user=user,
                nom=validated_data["nom"],
                prenom=validated_data["prenom"],
                email=validated_data["email"],
                telephone=validated_data.get("telephone", ""),
                ville=validated_data["ville"],
                region=validated_data["region"],
                specialite=validated_data["specialite"],
                secteur=validated_data["secteur"],
                diplome=validated_data.get("diplome"),
                statut="en_attente",
                date_inscription=timezone.now().date(),
            )
        return praticien