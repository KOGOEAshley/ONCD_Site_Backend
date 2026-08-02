from django.db import models


class Evenement(models.Model):
    CATEGORIE_CHOICES = [
        ("Congrès", "Congrès"),
        ("Atelier", "Atelier"),
        ("Webinaire", "Webinaire"),
        ("DPC", "DPC"),
    ]

    titre = models.CharField(max_length=250)
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES)
    date_debut = models.DateField()
    date_fin = models.DateField(blank=True, null=True, help_text="Laisser vide si l'événement dure un seul jour.")
    lieu = models.CharField(max_length=200)
    prix = models.CharField(max_length=50, help_text="Ex: '85 000 FCFA' ou 'Gratuit (membres)'")
    tags = models.CharField(max_length=250, blank=True, help_text="Séparés par des virgules, ex: Implantologie, Endodontie")
    places_totales = models.PositiveIntegerField()
    places_prises = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False, help_text="Affiché en grand format 'Événement Phare' en haut de page.")
    description = models.TextField(blank=True, help_text="Programme détaillé, affiché au clic sur 'Détails'.")

    class Meta:
        ordering = ["date_debut"]

    @property
    def places_restantes(self):
        return max(0, self.places_totales - self.places_prises)

    def __str__(self):
        return self.titre