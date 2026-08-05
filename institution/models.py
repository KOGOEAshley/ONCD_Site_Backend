from django.db import models


class MembreConseil(models.Model):
    nom = models.CharField(max_length=150, help_text="Ex: Dr. Adama Kaboré")
    fonction = models.CharField(max_length=100, help_text="Ex: Président, Vice-Président, Trésorier...")
    region = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="conseil/", blank=True, null=True, help_text="Facultatif : initiales affichées si absente.")
    ordre_affichage = models.PositiveIntegerField(default=0, help_text="Les membres avec le plus petit nombre s'affichent en premier.")

    class Meta:
        ordering = ["ordre_affichage", "nom"]
        verbose_name = "Membre du Conseil"
        verbose_name_plural = "Membres du Conseil"

    def __str__(self):
        return f"{self.nom} — {self.fonction}"