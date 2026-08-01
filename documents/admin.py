from django.contrib import admin
from .models import ModeleDocument


@admin.register(ModeleDocument)
class ModeleDocumentAdmin(admin.ModelAdmin):
    list_display = ["titre", "code", "actif"]
    prepopulated_fields = {"code": ("titre",)}