"""
schéma DB du catalogue, modèles Marque et Vehicule avec mode achat/location, motorisation, prix
sans ces models pas de table pour stocker les voitures donc pas de catalogue donc pas de site
utilisé par vehicles/views.py catalogue, dossiers/models.py ForeignKey Vehicule, seed_data.py alimente la DB

"""
from django.db import models

# https://github.com/django/djangoproject.com/blob/main/checklists/models.py

class Marque(models.Model):
    nom = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["nom"]

    def __str__(self):
        return self.nom

"""
textChoices à l'intérieur du model l'enum reste collée à son contexte
on l'utilise ensuite via Vehicule.ModeChoices.ACHAT c'est plus lisible
https://docs.djangoproject.com/en/6.0/ref/models/fields/#enumeration-types
"""
class Vehicule(models.Model):

    class ModeChoices(models.TextChoices):
        ACHAT = "achat", "Achat"
        LOCATION = "location", "Location"

    class MotorisationChoices(models.TextChoices):
        ESSENCE = "essence", "Essence"
        DIESEL = "diesel", "Diesel"
        HYBRIDE = "hybride", "Hybride"
        ELECTRIQUE = "electrique", "Électrique"

    marque = models.ForeignKey(Marque, on_delete=models.CASCADE, related_name="vehicules")
    modele = models.CharField(max_length=100)
    annee = models.PositiveIntegerField()
    kilometrage = models.PositiveIntegerField()
    motorisation = models.CharField(max_length=20, choices=MotorisationChoices.choices)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    loyer_mensuel = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    mode = models.CharField(max_length=10, choices=ModeChoices.choices)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to="vehicules/", blank=True)
    nom_complet = models.CharField(max_length=200, blank=True)
    image_slug = models.SlugField(max_length=250, blank=True)
    boite = models.CharField(max_length=50, blank=True)
    portes = models.PositiveSmallIntegerField(null=True, blank=True)
    puissance_fiscale = models.CharField(max_length=20, blank=True)
    puissance_din = models.CharField(max_length=20, blank=True)
    consommation = models.CharField(max_length=30, blank=True)
    disponible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.marque} {self.modele} ({self.annee})"

    """
    property plutôt qu'une méthode pour pouvoir l'appeler sans parenthèses dans le template
    toute la règle "vente vs LLD" est centralisé cii
    le - évite un affichage cassé si le prix n'a pas été saisi côté admin
    """
    @property
    def prix_affiche(self):
        if self.mode == self.ModeChoices.LOCATION:
            return f"{self.loyer_mensuel} € / mois" if self.loyer_mensuel else "-"
        return f"{self.prix_vente} €" if self.prix_vente else "-"