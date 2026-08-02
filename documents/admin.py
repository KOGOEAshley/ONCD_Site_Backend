from django.contrib import admin
from .models import ModeleDocument, DocumentTelechargeable


@admin.register(ModeleDocument)
class ModeleDocumentAdmin(admin.ModelAdmin):
    list_display = ["titre", "code", "actif"]
    prepopulated_fields = {"code": ("titre",)}


@admin.register(DocumentTelechargeable)
class DocumentTelechargeableAdmin(admin.ModelAdmin):
    list_display = ["titre", "categorie", "type_fichier", "taille_affichee", "date_maj"]
    list_filter = ["categorie"]
    search_fields = ["titre"]