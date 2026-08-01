from django.db import models
from praticiens.models import Praticien


class Formation(models.Model):
    nom = models.CharField(max_length=200)
    date_debut = models.DateField()
    date_fin = models.DateField()
    heures = models.PositiveIntegerField(help_text="Nombre d'heures DPC validées par cette formation")
    lieu = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.nom


class Participation(models.Model):
    """Relie un praticien à une formation qu'il a suivie (table intermédiaire)."""

    praticien = models.ForeignKey(Praticien, on_delete=models.CASCADE, related_name="participations")
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name="participations")
    heures_obtenues = models.PositiveIntegerField()
    valide = models.BooleanField(default=True)

    class Meta:
        unique_together = ("praticien", "formation")

    def __str__(self):
        return f"{self.praticien} — {self.formation}"