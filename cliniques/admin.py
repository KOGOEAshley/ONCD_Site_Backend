from django.contrib import admin
from .models import Clinique


@admin.register(Clinique)
class CliniqueAdmin(admin.ModelAdmin):
    list_display = ["nom", "ville", "quartier", "est_de_garde"]
    list_filter = ["ville", "est_de_garde", "region"]
    search_fields = ["nom", "adresse", "ville"]
    filter_horizontal = ["praticiens"]

    class Media:
        css = {
            "all": ("https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",)
        }
        js = (
            "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js",
            "cliniques/admin_map.js",
        )