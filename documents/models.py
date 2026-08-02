import os

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


class DocumentTelechargeable(models.Model):
    """
    Bibliothèque de fichiers téléchargeables (contrats types, guides, chartes...).
    Un seul modèle sert plusieurs sections du site (Modèles Juridiques pour les
    praticiens, Ressources pour les étudiants...), différenciées par 'categorie'.
    """

    CATEGORIE_CHOICES = [
        ("juridique", "Modèles Juridiques (Praticiens)"),
        ("etudiant", "Ressources Étudiantes"),
    ]

    titre = models.CharField(max_length=200)
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES)
    fichier = models.FileField(upload_to="bibliotheque/")
    date_maj = models.DateField(auto_now=True, help_text="Mise à jour automatique à chaque modification.")

    class Meta:
        ordering = ["categorie", "titre"]

    @property
    def type_fichier(self):
        _, ext = os.path.splitext(self.fichier.name)
        return ext.replace(".", "").upper() if ext else "FICHIER"

    @property
    def taille_affichee(self):
        try:
            taille_octets = self.fichier.size
        except (ValueError, FileNotFoundError):
            return "—"
        if taille_octets < 1024 * 1024:
            return f"{round(taille_octets / 1024)} Ko"
        return f"{round(taille_octets / (1024 * 1024), 1)} Mo"

    def __str__(self):
        return self.titre