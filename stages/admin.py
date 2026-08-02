from django.contrib import admin
from .models import Stage, CandidatureStage


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ["etablissement", "ville", "specialite", "niveau_requis", "places_restantes"]
    list_filter = ["ville", "specialite"]
    search_fields = ["etablissement", "ville"]


@admin.register(CandidatureStage)
class CandidatureStageAdmin(admin.ModelAdmin):
    list_display = ["nom", "prenom", "stage", "niveau_actuel", "statut", "date_candidature"]
    list_filter = ["statut", "stage"]
    search_fields = ["nom", "prenom", "email"]