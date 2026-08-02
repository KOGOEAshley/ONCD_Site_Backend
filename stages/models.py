from django.db import models


class Stage(models.Model):
    etablissement = models.CharField(max_length=200)
    ville = models.CharField(max_length=100)
    specialite = models.CharField(max_length=150)
    periode = models.CharField(max_length=100, help_text="Ex: Sep–Déc 2025")
    niveau_requis = models.CharField(max_length=50, help_text="Ex: D3 / D4")
    places_totales = models.PositiveIntegerField()
    places_prises = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["etablissement"]

    @property
    def places_restantes(self):
        return max(0, self.places_totales - self.places_prises)

    def __str__(self):
        return f"{self.etablissement} — {self.specialite}"


class CandidatureStage(models.Model):
    STATUT_CHOICES = [
        ("en_attente", "En attente"),
        ("acceptee", "Acceptée"),
        ("refusee", "Refusée"),
    ]

    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name="candidatures")
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20, blank=True)
    niveau_actuel = models.CharField(max_length=50, help_text="Ex: D3")
    cv = models.FileField(upload_to="candidatures_stages/", blank=True, null=True)
    message = models.TextField(blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default="en_attente")
    date_candidature = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_candidature"]

    def __str__(self):
        return f"{self.prenom} {self.nom} — {self.stage}"