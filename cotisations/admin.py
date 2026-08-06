from django.contrib import admin, messages
from django.utils import timezone

from praticiens.models import Praticien
from .models import BaremeCotisation, Cotisation


@admin.register(BaremeCotisation)
class BaremeCotisationAdmin(admin.ModelAdmin):
    list_display = ["secteur", "montant"]
    list_editable = ["montant"]


@admin.action(description="Marquer comme payée (aujourd'hui)")
def marquer_payee(modeladmin, request, queryset):
    queryset.update(statut="payee", date_paiement=timezone.now().date())
    modeladmin.message_user(request, f"{queryset.count()} cotisation(s) marquée(s) comme payée(s).")


@admin.action(description="Générer les cotisations de l'année en cours pour tous les praticiens actifs")
def generer_cotisations_annee(modeladmin, request, queryset):
    annee = timezone.now().year
    praticiens_actifs = Praticien.objects.filter(statut="actif")
    creees = 0
    for praticien in praticiens_actifs:
        _, cree = Cotisation.objects.get_or_create(
            praticien=praticien,
            annee=annee,
            defaults={"montant": 0},
        )
        if cree:
            creees += 1
    modeladmin.message_user(
        request,
        f"{creees} nouvelle(s) cotisation(s) {annee} créée(s) "
        f"(les praticiens qui avaient déjà une cotisation {annee} n'ont pas été dupliqués).",
        level=messages.SUCCESS,
    )


@admin.register(Cotisation)
class CotisationAdmin(admin.ModelAdmin):
    list_display = ["praticien", "annee", "montant", "date_echeance", "statut"]
    list_filter = ["statut", "annee"]
    search_fields = ["praticien__nom", "praticien__prenom", "praticien__numero_inscription"]
    actions = [marquer_payee, generer_cotisations_annee]