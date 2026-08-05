from django.contrib import admin
from .models import MembreConseil


@admin.register(MembreConseil)
class MembreConseilAdmin(admin.ModelAdmin):
    list_display = ["nom", "fonction", "region", "ordre_affichage"]
    list_editable = ["ordre_affichage"]
    search_fields = ["nom", "fonction"]