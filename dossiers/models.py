"""
schéma DB des dossiers DossierBase mutualise les 4 doc + statut, hérité par DossierAchat et DossierLocation
sans ces models pas de persistance des demandes client donc le site sert à rien
ForeignKey vers User settings.AUTH_USER_MODEL et vehicles.Vehicule lus par dossiers/views.py et accounts/views.py
"""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

# https://github.com/django/djangoproject.com/blob/main/blog/models.py

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 Mo
ALLOWED_EXTENSIONS = (".pdf", ".jpg", ".jpeg", ".png")

"""
https://docs.djangoproject.com/en/6.0/ref/validators/#writing-validators
"""

def valider_document(fichier):
    if fichier.size > MAX_FILE_SIZE:
        raise ValidationError("Fichier trop volumineux (max 5 Mo).")
    if not fichier.name.lower().endswith(ALLOWED_EXTENSIONS):
        raise ValidationError("Format invalide. Formats autorisés : PDF, JPG, PNG.")

"""
modèle pour mutualiser les 4 doc + statut + le lien client/véhicule
achat et Location partagent 90% du schéma, mais on veut deux tables séparées plutôt
qu'un héritage multitable, ça garde les requêtes simples et évite un JOIN partout.
https://docs.djangoproject.com/en/6.0/topics/db/models/#abstract-base-classes
"""

class DossierBase(models.Model):
    class StatutChoices(models.TextChoices):
        DEPOSE = "depose", "Déposé"
        EN_TRAITEMENT = "en_traitement", "En traitement"
        VALIDE = "valide", "Validé"
        REFUSE = "refuse", "Refusé"

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vehicule = models.ForeignKey("vehicles.Vehicule", on_delete=models.CASCADE)
    statut = models.CharField(
        max_length=20, choices=StatutChoices.choices, default=StatutChoices.DEPOSE
    )
    cni = models.FileField(upload_to="documents/", validators=[valider_document])
    justificatif_domicile = models.FileField(upload_to="documents/", validators=[valider_document])
    rib = models.FileField(upload_to="documents/", validators=[valider_document])
    justificatif_revenus = models.FileField(upload_to="documents/", validators=[valider_document])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]


class DossierAchat(DossierBase):
    reprise_vehicule = models.BooleanField(default=False)

    def __str__(self):
        return f"Achat #{self.pk} - {self.client.username}"


class DossierLocation(DossierBase):
    class DureeChoices(models.IntegerChoices):
        MOIS_12 = 12, "12 mois"
        MOIS_24 = 24, "24 mois"
        MOIS_36 = 36, "36 mois"
        MOIS_48 = 48, "48 mois"

    duree_mois = models.IntegerField(choices=DureeChoices.choices)
    assurance = models.BooleanField(default=False)
    entretien = models.BooleanField(default=False)

    def __str__(self):
        return f"Location #{self.pk} - {self.client.username}"

    """
        calcul du loyer final côté model (pas dans le template)
        forfaits +30/+25 en dur, c'est ce que demande le cahier des charges si un jour
        ça devient variable faudra une table Option dédiée
    """

    @property
    def loyer_total(self):
        if not self.vehicule.loyer_mensuel:
            return None
        base = float(self.vehicule.loyer_mensuel)
        if self.assurance:
            base += 30
        if self.entretien:
            base += 25
        return round(base, 2)