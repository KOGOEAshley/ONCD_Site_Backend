from django.conf import settings
from django.db import models
from django.utils import timezone


class Praticien(models.Model):
    STATUT_CHOICES = [
        ("en_attente", "En attente de validation"),
        ("actif", "Actif"),
        ("suspendu", "Suspendu"),
        ("radie", "Radié"),
        ("refuse", "Demande refusée"),
    ]

    SECTEUR_CHOICES = [
        ("liberal", "Chirurgien-Dentiste libéral"),
        ("secteur_public", "Salarié secteur public"),
        ("secteur_prive", "Salarié secteur privé"),
        ("mixte", "Exercice mixte"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="praticien",
        null=True,
        blank=True,
    )

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    numero_inscription = models.CharField(max_length=20, unique=True, blank=True, null=True)
    ville = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    specialite = models.CharField(max_length=150)
    secteur = models.CharField(max_length=20, choices=SECTEUR_CHOICES, default="liberal")
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="en_attente")
    date_inscription = models.DateField()
    photo = models.ImageField(upload_to="praticiens/", blank=True, null=True)
    diplome = models.FileField(upload_to="diplomes/", blank=True, null=True)

    class Meta:
        ordering = ["nom", "prenom"]

    def save(self, *args, **kwargs):
        # Dès qu'un dossier passe au statut "Actif" (validation par le secrétariat),
        # on lui attribue automatiquement un numéro s'il n'en a pas déjà un.
        if self.statut == "actif" and not self.numero_inscription:
            annee = (self.date_inscription or timezone.now().date()).year
            prefixe = f"ONCD-{annee}-"

            dernier = (
                Praticien.objects.filter(numero_inscription__startswith=prefixe)
                .exclude(pk=self.pk)
                .order_by("-numero_inscription")
                .first()
            )

            dernier_num = 0
            if dernier and dernier.numero_inscription:
                try:
                    dernier_num = int(dernier.numero_inscription.split("-")[-1])
                except ValueError:
                    dernier_num = 0

            self.numero_inscription = f"{prefixe}{dernier_num + 1:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Dr {self.prenom} {self.nom} ({self.ville})"