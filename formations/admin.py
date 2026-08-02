import csv
import io
import zipfile

from django.contrib import admin, messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import path
from django.utils import timezone

from documents.models import ModeleDocument
from documents.services import rendre_modele, generer_pdf_depuis_html
from praticiens.models import Praticien

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
            level=messages.ERROR,
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
    search_fields = ["praticien__nom", "praticien__prenom", "praticien__numero_inscription"]
    actions = [telecharger_attestations_zip]
    change_list_template = "formations/participation_changelist.html"

    def get_urls(self):
        urls_perso = [
            path(
                "importer-csv/",
                self.admin_site.admin_view(self.importer_csv),
                name="formations_participation_importer_csv",
            ),
        ]
        return urls_perso + super().get_urls()

    def importer_csv(self, request):
        if request.method == "POST":
            fichier = request.FILES.get("fichier_csv")
            if not fichier:
                messages.error(request, "Aucun fichier sélectionné.")
                return HttpResponseRedirect("../")

            donnees = io.TextIOWrapper(fichier.file, encoding="utf-8-sig")
            lecteur = csv.DictReader(donnees)

            crees = 0
            mis_a_jour = 0
            erreurs = []

            for i, ligne in enumerate(lecteur, start=2):
                numero = (ligne.get("numero_inscription") or "").strip()
                nom_formation = (ligne.get("formation") or "").strip()
                heures = (ligne.get("heures_obtenues") or "").strip()

                if not numero or not nom_formation:
                    erreurs.append(f"Ligne {i} : numero_inscription ou formation manquant.")
                    continue

                try:
                    praticien = Praticien.objects.get(numero_inscription=numero)
                except Praticien.DoesNotExist:
                    erreurs.append(f"Ligne {i} : aucun praticien avec le numéro '{numero}'.")
                    continue

                try:
                    formation = Formation.objects.get(nom=nom_formation)
                except Formation.DoesNotExist:
                    erreurs.append(f"Ligne {i} : aucune formation nommée '{nom_formation}'.")
                    continue

                try:
                    heures_val = int(heures) if heures else formation.heures
                except ValueError:
                    heures_val = formation.heures

                _, cree = Participation.objects.update_or_create(
                    praticien=praticien,
                    formation=formation,
                    defaults={"heures_obtenues": heures_val, "valide": True},
                )
                if cree:
                    crees += 1
                else:
                    mis_a_jour += 1

            if crees or mis_a_jour:
                messages.success(request, f"{crees} participation(s) créée(s), {mis_a_jour} mise(s) à jour.")
            if erreurs:
                apercu = " | ".join(erreurs[:10])
                suite = " ..." if len(erreurs) > 10 else ""
                messages.warning(request, f"{len(erreurs)} ligne(s) ignorée(s) : {apercu}{suite}")

            return HttpResponseRedirect("../")

        return render(request, "formations/importer_csv.html", {"title": "Importer des participations (CSV)"})