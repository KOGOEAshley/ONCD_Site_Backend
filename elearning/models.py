from django.db import models
from praticiens.models import Praticien


class ModuleELearning(models.Model):
    NIVEAU_CHOICES = [
        ("Débutant", "Débutant"),
        ("Intermédiaire", "Intermédiaire"),
        ("Avancé", "Avancé"),
        ("Obligatoire", "Obligatoire"),
    ]

    titre = models.CharField(max_length=250)
    duree = models.CharField(max_length=20, help_text="Ex: '4h30'")
    niveau = models.CharField(max_length=20, choices=NIVEAU_CHOICES)
    description = models.TextField(blank=True)
    lien_video = models.URLField(blank=True, help_text="Lien vers le module (YouTube non répertorié, Vimeo...).")

    def __str__(self):
        return self.titre


class InscriptionModule(models.Model):
    praticien = models.ForeignKey(Praticien, on_delete=models.CASCADE, related_name="modules_elearning")
    module = models.ForeignKey(ModuleELearning, on_delete=models.CASCADE, related_name="inscriptions")
    date_inscription = models.DateTimeField(auto_now_add=True)
    termine = models.BooleanField(default=False)
    date_completion = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ("praticien", "module")

    def __str__(self):
        return f"{self.praticien} — {self.module}"