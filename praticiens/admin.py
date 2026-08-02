from django.contrib import admin
from .models import Praticien


@admin.register(Praticien)
class PraticienAdmin(admin.ModelAdmin):
    # Colonnes affichées dans la liste
    list_display = ["nom", "prenom", "ville", "specialite", "secteur", "statut", "numero_inscription"]
    # Filtres dans la barre latérale
    list_filter = ["statut", "region", "secteur"]
    # Barre de recherche
    search_fields = ["nom", "prenom", "numero_inscription"]
