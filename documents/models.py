from django.db import models


class ModeleDocument(models.Model):
    code = models.SlugField(
        max_length=50,
        unique=True,
        help_text="Identifiant technique unique, ex: attestation_formation_anesthesie",
    )
    titre = models.CharField(max_length=150)
    corps_html = models.TextField(
        help_text=(
            "Contenu HTML du document (utilisez les mêmes styles CSS que les autres modèles). "
            "Variables disponibles pour un praticien : {{ praticien.nom }}, {{ praticien.prenom }}, "
            "{{ praticien.numero_inscription }}, {{ praticien.specialite }}, {{ praticien.ville }}, "
            "{{ date_edition }}. Pour une attestation de formation, en plus : "
            "{{ participation.formation.nom }}, {{ participation.formation.date_debut }}, "
            "{{ participation.formation.date_fin }}, {{ participation.heures_obtenues }}."
        )
    )
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Modèle de document"
        verbose_name_plural = "Modèles de documents"

    def __str__(self):
        return self.titre