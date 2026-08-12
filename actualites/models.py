import math

from django.db import models
from django.utils import timezone


class Actualite(models.Model):
    CATEGORIE_CHOICES = [
        ("Formation", "Formation"),
        ("Réglementation", "Réglementation"),
        ("Alerte sanitaire", "Alerte sanitaire"),
        ("Santé publique", "Santé publique"),
        ("International", "International"),
        ("Déontologie", "Déontologie"),
    ]

    titre = models.CharField(max_length=250)
    categorie = models.CharField(max_length=30, choices=CATEGORIE_CHOICES)
    extrait = models.TextField(help_text="Court résumé affiché dans les listes (1-2 phrases).")
    contenu = models.TextField(help_text="Texte complet de l'article.", blank=True)
    auteur = models.CharField(max_length=150, blank=True)
    image = models.ImageField(
        upload_to="actualites/",
        blank=True,
        null=True,
        help_text="Photo affichée juste après le titre de l'article (facultatif).",
    )
    a_la_une = models.BooleanField(
        default=False,
        help_text="Une seule actualité à la fois devrait être 'à la une' idéalement.",
    )
    date_publication = models.DateField(default=timezone.now)
    temps_lecture = models.CharField(
        max_length=20,
        blank=True,
        help_text="Calculé automatiquement si laissé vide (ex: '3 min').",
    )

    class Meta:
        ordering = ["-date_publication"]

    def save(self, *args, **kwargs):
        if not self.temps_lecture:
            nb_mots = len((self.contenu or self.extrait).split())
            minutes = max(1, math.ceil(nb_mots / 200))
            self.temps_lecture = f"{minutes} min"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre