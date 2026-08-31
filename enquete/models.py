from django.db import models


class FicheCollecteDonnees(models.Model):
    """
    Fiche de collecte de données de l'état des lieux de l'offre des soins
    bucco-dentaires au Burkina Faso (Octobre 2025).
    Reproduit fidèlement les 9 sections du questionnaire papier fourni par l'Ordre.
    """

    STATUT_PRO_CHOICES = [("agent_etat", "Agent de l'État"), ("agent_prive", "Agent du secteur privé")]
    TYPE_STRUCTURE_CHOICES = [("publique", "Publique"), ("privee", "Privée")]
    OUI_NON_CHOICES = [("oui", "Oui"), ("non", "Non")]
    FREQUENTATION_CHOICES = [
        ("moins_5_semaine", "Moins de 5 patients par semaine"),
        ("1_5_jour", "Entre 1 et 5 patients par jour"),
        ("5_10_jour", "Entre 5 et 10 patients par jour"),
        ("10_20_jour", "Entre 10 et 20 patients par jour"),
        ("plus_20_jour", "Plus de 20 patients par jour"),
    ]
    REGULARITE_CHOICES = [
        ("semestre", "Une fois par semestre"),
        ("an", "Une fois par an"),
        ("2_3_ans", "Tous les 2 à 3 ans"),
        ("rarement", "Rarement"),
    ]
    DUREE_REPARATION_CHOICES = [
        ("1_2_semaines", "1 à 2 semaines"),
        ("plus_1_mois", "Plus d'un mois"),
        ("3_mois_plus", "Trois mois et plus"),
        ("1_an_plus", "Un an et plus"),
    ]
    NB_FORMATIONS_CHOICES = [
        ("aucune", "Aucune"), ("1_2", "1-2"), ("3_5", "3-5"), ("plus_5", "Plus de 5"),
    ]
    NIVEAU_IMPACT_CHOICES = [
        ("beaucoup", "Beaucoup"), ("moyennement", "Moyennement"), ("peu", "Peu"), ("pas_du_tout", "Pas du tout"),
    ]
    ADEQUATION_CHOICES = [("oui", "Oui"), ("partiellement", "Partiellement"), ("non", "Non")]

    # --- I. Données socioprofessionnelles du répondant ---
    nom_repondant = models.CharField(max_length=200)
    annee_diplome = models.CharField(max_length=10, blank=True)
    denomination_diplome = models.CharField(max_length=255, blank=True)
    lieu_diplome = models.CharField(max_length=255, blank=True)
    statut_professionnel = models.CharField(max_length=20, choices=STATUT_PRO_CHOICES, blank=True)

    # --- II.1 Identification de la structure ---
    denomination_structure = models.CharField(max_length=255, blank=True)
    type_structure = models.CharField(max_length=20, choices=TYPE_STRUCTURE_CHOICES, blank=True)
    region_sanitaire = models.CharField(max_length=150, blank=True)
    district_sanitaire = models.CharField(max_length=150, blank=True)
    cabinet_fonctionnel_public = models.CharField(
        max_length=5, choices=OUI_NON_CHOICES, blank=True,
        help_text="Structures publiques uniquement : cabinet dentaire fonctionnel présent ?",
    )
    description_batiment = models.TextField(blank=True, help_text="Superficie, ventilation, état général, nb de salles de soins.")

    # --- II.2 Ressources humaines du cabinet ---
    nb_dentistes = models.PositiveIntegerField(null=True, blank=True)
    nb_attaches_assistants = models.PositiveIntegerField(null=True, blank=True)
    personnel_soutien_nombre = models.PositiveIntegerField(null=True, blank=True)
    personnel_soutien_profil = models.CharField(max_length=255, blank=True)
    personnel_soutien_role = models.CharField(max_length=255, blank=True)

    # --- II.3 Équipements et matériels dentaires ---
    nb_fauteuils_total = models.PositiveIntegerField(null=True, blank=True)
    nb_fauteuils_fonctionnels = models.PositiveIntegerField(null=True, blank=True)
    annee_dernier_fauteuil = models.CharField(max_length=10, blank=True)
    structure_donatrice = models.CharField(max_length=255, blank=True)

    # Tableau "Autres équipements" : { "Autoclave": {"nombre": "2", "fonctionnel": "oui", "annee": "2022"}, ... }
    equipements_autres = models.JSONField(default=dict, blank=True)

    # --- II.4 Instruments et consommables dentaires ---
    # { "Daviers": {"situation": "suffisant|insuffisant|rupture", "date_dotation": "..."}, ... }
    instruments_consommables = models.JSONField(default=dict, blank=True)

    # --- II.5 Approvisionnement et gestion des consommables ---
    responsable_gestion_materiel = models.CharField(max_length=100, blank=True)
    responsable_gestion_materiel_autre = models.CharField(max_length=255, blank=True)
    responsable_commandes = models.CharField(max_length=100, blank=True)
    responsable_commandes_autre = models.CharField(max_length=255, blank=True)
    regularite_approvisionnement = models.CharField(max_length=20, choices=REGULARITE_CHOICES, blank=True)
    plafond_budgetaire = models.CharField(max_length=5, choices=OUI_NON_CHOICES, blank=True)
    plafond_budgetaire_precision = models.CharField(max_length=255, blank=True)

    # --- II.6 Maintenance des équipements ---
    panne_fauteuil = models.CharField(max_length=5, choices=OUI_NON_CHOICES, blank=True)
    type_panne = models.CharField(max_length=100, blank=True)
    type_panne_autre = models.CharField(max_length=255, blank=True)
    duree_reparation = models.CharField(max_length=20, choices=DUREE_REPARATION_CHOICES, blank=True)

    # --- III. Exercice de la chirurgie dentaire dans l'aire sanitaire ---
    soins_offerts = models.JSONField(default=list, blank=True, help_text="Liste des types de soins cochés.")
    soins_offerts_autre = models.CharField(max_length=255, blank=True)
    frequentation = models.CharField(max_length=20, choices=FREQUENTATION_CHOICES, blank=True)
    autres_cabinets_existent = models.CharField(max_length=5, choices=OUI_NON_CHOICES, blank=True)
    autres_cabinets_nombre = models.PositiveIntegerField(null=True, blank=True)
    # Liste de { "type": "Public|Privé", "appreciation": "texte" }
    cabinets_appreciation = models.JSONField(default=list, blank=True)

    # --- IV. Accès et participation à la formation continue ---
    formation_recente_12mois = models.CharField(max_length=5, choices=OUI_NON_CHOICES, blank=True)
    nb_formations_3ans = models.CharField(max_length=20, choices=NB_FORMATIONS_CHOICES, blank=True)
    formes_formations = models.JSONField(default=list, blank=True)
    organisateurs_formations = models.JSONField(default=list, blank=True)
    organisateurs_formations_autre = models.CharField(max_length=255, blank=True)

    # --- V. Domaines de formation suivis ou souhaités ---
    domaines_formes = models.JSONField(default=list, blank=True)
    domaines_formes_autre = models.CharField(max_length=255, blank=True)
    besoins_formation = models.TextField(blank=True)

    # --- VI. Impact et utilité de la formation continue ---
    impact_formation = models.CharField(max_length=20, choices=NIVEAU_IMPACT_CHOICES, blank=True)
    formations_adaptees = models.CharField(max_length=20, choices=ADEQUATION_CHOICES, blank=True)
    difficultes_application = models.CharField(max_length=5, choices=OUI_NON_CHOICES, blank=True)
    difficultes_application_texte = models.TextField(blank=True)

    # --- VII. Formation continue du personnel des cabinets dentaires ---
    personnel_formation_continue = models.CharField(max_length=5, choices=OUI_NON_CHOICES, blank=True)
    agents_formes = models.JSONField(default=list, blank=True)
    agents_formes_autre = models.CharField(max_length=255, blank=True)

    # --- VIII. Pratiques illégales de la chirurgie dentaire ---
    pratique_illegale_connue = models.CharField(max_length=5, choices=OUI_NON_CHOICES, blank=True)
    pi_denomination_structure = models.CharField(max_length=255, blank=True)
    pi_position_geographique = models.CharField(max_length=255, blank=True)
    pi_identite_praticien = models.CharField(max_length=255, blank=True)
    pi_types_actes = models.CharField(max_length=255, blank=True)
    pi_autre_detail = models.TextField(blank=True)

    # --- IX. Difficultés et suggestions ---
    difficultes_structure = models.TextField(blank=True)
    suggestions_structure = models.TextField(blank=True)
    difficultes_pays = models.TextField(blank=True)
    suggestions_pays = models.TextField(blank=True)
    ampleur_pratique_illegale = models.TextField(blank=True)
    suggestions_pratique_illegale = models.TextField(blank=True)

    date_soumission = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_soumission"]
        verbose_name = "Fiche de collecte (offre de soins bucco-dentaires)"
        verbose_name_plural = "Fiches de collecte (offre de soins bucco-dentaires)"

    def __str__(self):
        return f"{self.nom_repondant} — {self.denomination_structure} ({self.date_soumission:%d/%m/%Y})"