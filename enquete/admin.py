from django.contrib import admin
from .models import FicheCollecteDonnees


@admin.register(FicheCollecteDonnees)
class FicheCollecteDonneesAdmin(admin.ModelAdmin):
    list_display = [
        "nom_repondant", "denomination_structure", "type_structure",
        "region_sanitaire", "date_soumission",
    ]
    list_filter = ["type_structure", "region_sanitaire", "statut_professionnel"]
    search_fields = ["nom_repondant", "denomination_structure", "region_sanitaire", "district_sanitaire"]
    readonly_fields = ["date_soumission"]

    fieldsets = (
        ("I. Répondant", {
            "fields": ("nom_repondant", "annee_diplome", "denomination_diplome", "lieu_diplome", "statut_professionnel"),
        }),
        ("II.1 Identification de la structure", {
            "fields": (
                "denomination_structure", "type_structure", "region_sanitaire", "district_sanitaire",
                "cabinet_fonctionnel_public", "description_batiment",
            ),
        }),
        ("II.2 Ressources humaines", {
            "fields": ("nb_dentistes", "nb_attaches_assistants", "personnel_soutien_nombre",
                       "personnel_soutien_profil", "personnel_soutien_role"),
        }),
        ("II.3 Équipements", {
            "fields": ("nb_fauteuils_total", "nb_fauteuils_fonctionnels", "annee_dernier_fauteuil",
                       "structure_donatrice", "equipements_autres"),
        }),
        ("II.4 Instruments et consommables", {"fields": ("instruments_consommables",)}),
        ("II.5 Approvisionnement", {
            "fields": ("responsable_gestion_materiel", "responsable_gestion_materiel_autre",
                       "responsable_commandes", "responsable_commandes_autre",
                       "regularite_approvisionnement", "plafond_budgetaire", "plafond_budgetaire_precision"),
        }),
        ("II.6 Maintenance", {"fields": ("panne_fauteuil", "type_panne", "type_panne_autre", "duree_reparation")}),
        ("III. Exercice de la chirurgie dentaire", {
            "fields": ("soins_offerts", "soins_offerts_autre", "frequentation",
                       "autres_cabinets_existent", "autres_cabinets_nombre", "cabinets_appreciation"),
        }),
        ("IV. Accès à la formation continue", {
            "fields": ("formation_recente_12mois", "nb_formations_3ans", "formes_formations",
                       "organisateurs_formations", "organisateurs_formations_autre"),
        }),
        ("V. Domaines de formation", {"fields": ("domaines_formes", "domaines_formes_autre", "besoins_formation")}),
        ("VI. Impact de la formation", {
            "fields": ("impact_formation", "formations_adaptees", "difficultes_application", "difficultes_application_texte"),
        }),
        ("VII. Formation du personnel", {
            "fields": ("personnel_formation_continue", "agents_formes", "agents_formes_autre"),
        }),
        ("VIII. Pratiques illégales", {
            "fields": ("pratique_illegale_connue", "pi_denomination_structure", "pi_position_geographique",
                       "pi_identite_praticien", "pi_types_actes", "pi_autre_detail"),
        }),
        ("IX. Difficultés et suggestions", {
            "fields": ("difficultes_structure", "suggestions_structure", "difficultes_pays", "suggestions_pays",
                       "ampleur_pratique_illegale", "suggestions_pratique_illegale"),
        }),
        ("Métadonnées", {"fields": ("date_soumission",)}),
    )