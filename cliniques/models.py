from django.db import models


class Clinique(models.Model):
    nom = models.CharField(max_length=150)
    adresse = models.CharField(max_length=255)
    ville = models.CharField(max_length=100)
    region = models.CharField(max_length=100, blank=True)   # ← vérifiez que cette ligne existe
    quartier = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    telephone = models.CharField(max_length=20, blank=True)
    horaires = models.CharField(max_length=255, blank=True)

    praticiens = models.ManyToManyField(
        "praticiens.Praticien",
        related_name="cliniques",
        blank=True,
    )

    est_de_garde = models.BooleanField(default=False)

    class Meta:
        ordering = ["ville", "nom"]

    def __str__(self):
        return f"{self.nom} — {self.ville}"