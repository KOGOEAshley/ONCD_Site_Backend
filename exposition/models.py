from django.db import models


class Exposant(models.Model):
    CATEGORIE_CHOICES = [
        ("Équipements", "Équipements"),
        ("Pharmacie", "Pharmacie"),
        ("Imagerie", "Imagerie"),
        ("Prothèse", "Prothèse"),
        ("Implants", "Implants"),
        ("Instrumentation", "Instrumentation"),
    ]

    nom = models.CharField(max_length=200)
    pays = models.CharField(max_length=100)
    categorie = models.CharField(max_length=30, choices=CATEGORIE_CHOICES)
    produits = models.CharField(max_length=300, help_text="Séparés par des virgules, ex: Fauteuils dentaires, Turbines")
    stand = models.CharField(max_length=20, unique=True, help_text="Ex: A-12")
    contact_email = models.EmailField()
    logo = models.ImageField(upload_to="exposants/", blank=True, null=True, help_text="Logo de l'entreprise (facultatif).")
    photo_stand = models.ImageField(
    upload_to="exposants/photos/",
    blank=True,
    null=True,
    help_text="Photo du stand ou des produits exposés (facultatif).",)

    class Meta:
        ordering = ["stand"]

    def __str__(self):
        return f"{self.nom} ({self.stand})"


class ReservationStand(models.Model):
    STATUT_CHOICES = [
        ("en_attente", "En attente"),
        ("confirmee", "Confirmée"),
        ("refusee", "Refusée"),
    ]

    nom_entreprise = models.CharField(max_length=200)
    email = models.EmailField()
    telephone = models.CharField(max_length=20, blank=True)
    pays = models.CharField(max_length=100)
    categorie_souhaitee = models.CharField(max_length=30, choices=Exposant.CATEGORIE_CHOICES)
    message = models.TextField(blank=True, help_text="Précisions sur les produits/besoins de l'entreprise.")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="en_attente")
    date_demande = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_demande"]

    def __str__(self):
        return f"{self.nom_entreprise} — {self.get_statut_display()}"