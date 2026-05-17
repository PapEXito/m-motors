"""
modelForms pour la création d'un DossierAchat ou DossierLocation côté client
convertit le POST client en instance de model avec les 4 docs requis + settings spécifiques (reprise, durée...
utilisé par dossiers/views.py link aux models dossiers/models.py
"""
from django import forms
from .models import DossierAchat, DossierLocation

class DossierAchatForm(forms.ModelForm):
    class Meta:
        model = DossierAchat
        fields = ("reprise_vehicule", "cni", "justificatif_domicile", "rib", "justificatif_revenus")


class DossierLocationForm(forms.ModelForm):
    class Meta:
        model = DossierLocation
        fields = (
            "duree_mois", "assurance", "entretien",
            "cni", "justificatif_domicile", "rib", "justificatif_revenus",
        )