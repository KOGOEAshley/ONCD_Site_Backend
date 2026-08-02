from django.contrib import admin
from .models import ModuleELearning, InscriptionModule


@admin.register(ModuleELearning)
class ModuleELearningAdmin(admin.ModelAdmin):
    list_display = ["titre", "niveau", "duree"]
    list_filter = ["niveau"]
    search_fields = ["titre"]


@admin.register(InscriptionModule)
class InscriptionModuleAdmin(admin.ModelAdmin):
    list_display = ["praticien", "module", "date_inscription", "termine"]
    list_filter = ["termine", "module"]
    search_fields = ["praticien__nom", "praticien__prenom"]