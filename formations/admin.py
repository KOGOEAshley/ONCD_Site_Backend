import io
import zipfile

from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone

from documents.models import ModeleDocument
from documents.services import rendre_modele, generer_pdf_depuis_html

from .models import Formation, Participation


@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ["nom", "date_debut", "date_fin", "heures", "lieu"]


@admin.action(description="Télécharger les attestations sélectionnées (ZIP)")
def telecharger_attestations_zip(modeladmin, request, queryset):
    try:
        modele = ModeleDocument.objects.get(code="attestation_formation", actif=True)
    except ModeleDocument.DoesNotExist:
        modeladmin.message_user(
            request,
            "Aucun modèle actif avec le code 'attestation_formation'. "
            "Créez-le dans Documents > Modèles de documents.",
            level="error",
        )
        return

    buffer_zip = io.BytesIO()
    with zipfile.ZipFile(buffer_zip, "w") as archive:
        for participation in queryset:
            html = rendre_modele(modele, {
                "praticien": participation.praticien,
                "participation": participation,
                "date_edition": timezone.now().date(),
            })
            pdf_bytes = generer_pdf_depuis_html(html)
            identifiant = participation.praticien.numero_inscription or participation.praticien.id
            nom_fichier = f"{identifiant}_{participation.formation.nom}.pdf".replace(" ", "_")
            archive.writestr(nom_fichier, pdf_bytes)

    buffer_zip.seek(0)
    reponse = HttpResponse(buffer_zip, content_type="application/zip")
    reponse["Content-Disposition"] = 'attachment; filename="attestations.zip"'
    return reponse


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ["praticien", "formation", "heures_obtenues", "valide"]
    list_filter = ["formation", "valide"]
    search_fields = ["praticien__nom", "praticien__prenom"]
    actions = [telecharger_attestations_zip]