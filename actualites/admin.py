from django.contrib import admin
from .models import Actualite


@admin.register(Actualite)
class ActualiteAdmin(admin.ModelAdmin):
    list_display = ["titre", "categorie", "date_publication", "a_la_une", "temps_lecture"]
    list_filter = ["categorie", "a_la_une"]
    search_fields = ["titre", "extrait", "contenu"]
    date_hierarchy = "date_publication"