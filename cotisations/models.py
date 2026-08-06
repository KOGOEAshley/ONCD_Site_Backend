from datetime import date

from django.db import models
from praticiens.models import Praticien


class BaremeCotisation(models.Model):
    """
    Montant de la cotisation selon le secteur d'exercice.
    Éditable depuis l'admin — remplace un barème fixe codé en dur,
    pour pouvoir ajuster les tarifs d'une année sur l'autre sans toucher au code.
    """

    secteur = models.CharField(max_length=20, choices=Praticien.SECTEUR_CHOICES, unique=True)
    montant = models.PositiveIntegerField(help_text="Montant annuel en FCFA.")

    class Meta:
        verbose_name = "Barème de cotisation"
        verbose_name_plural = "Barème des cotisations"

    def __str__(self):
        return f"{self.get_secteur_display()} — {self.montant:,} FCFA".replace(",", " ")


def echeance_par_defaut():
    """31 mars de l'année en cours — fonction nommée (pas une lambda) car
    Django doit pouvoir l'enregistrer telle quelle dans les fichiers de migration."""
    return date(date.today().year, 3, 31)


class Cotisation(models.Model):
    STATUT_CHOICES = [
        ("en_attente", "En attente"),
        ("payee", "Payée"),
        ("en_retard", "En retard"),
    ]

    METHODE_CHOICES = [
        ("especes", "Espèces"),
        ("virement", "Virement bancaire"),
        ("mobile_money", "Mobile Money"),
        ("autre", "Autre"),
    ]

    praticien = models.ForeignKey(Praticien, on_delete=models.CASCADE, related_name="cotisations")
    annee = models.PositiveIntegerField()
    montant = models.PositiveIntegerField(help_text="En FCFA. Calculé automatiquement selon le secteur si laissé à 0.")
    date_echeance = models.DateField(default=echeance_par_defaut)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="en_attente")
    date_paiement = models.DateField(blank=True, null=True)
    methode_paiement = models.CharField(max_length=20, choices=METHODE_CHOICES, blank=True)
    reference = models.CharField(max_length=100, blank=True, help_text="N° de reçu, référence de virement, etc.")

    class Meta:
        unique_together = ("praticien", "annee")
        ordering = ["-annee", "praticien__nom"]

    def save(self, *args, **kwargs):
        if not self.montant:
            bareme = BaremeCotisation.objects.filter(secteur=self.praticien.secteur).first()
            self.montant = bareme.montant if bareme else 0

        if self.statut == "en_attente" and self.date_echeance < date.today():
            self.statut = "en_retard"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.praticien} — Cotisation {self.annee}"