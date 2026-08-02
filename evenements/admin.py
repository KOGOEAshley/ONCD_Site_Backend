from django.contrib import admin
from .models import Evenement


@admin.register(Evenement)
class EvenementAdmin(admin.ModelAdmin):
    list_display = ["titre", "categorie", "date_debut", "lieu", "places_restantes", "featured"]
    list_filter = ["categorie", "featured"]
    search_fields = ["titre", "lieu", "tags"]