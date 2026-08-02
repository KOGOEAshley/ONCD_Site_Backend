from django.contrib import admin
from .models import Exposant, ReservationStand


@admin.register(Exposant)
class ExposantAdmin(admin.ModelAdmin):
    list_display = ["nom", "stand", "categorie", "pays"]
    list_filter = ["categorie", "pays"]
    search_fields = ["nom", "stand"]


@admin.register(ReservationStand)
class ReservationStandAdmin(admin.ModelAdmin):
    list_display = ["nom_entreprise", "categorie_souhaitee", "pays", "statut", "date_demande"]
    list_filter = ["statut", "categorie_souhaitee"]
    search_fields = ["nom_entreprise", "email"]