"""
enregistre les modèles Marque et Vehicule dans /admin/ avec filtres et recherche
permet de gérer le catalogue depuis l'ui django sans toucher au code ajouter, modifier, désactiver une voiture
utilise vehicles/models.py accessible via /admin/ déclaré dans config/urls.py

"""
from django.contrib import admin
from .models import Marque, Vehicule

# https://github.com/django/djangoproject.com/blob/main/checklists/admin.py

@admin.register(Marque)
class MarqueAdmin(admin.ModelAdmin):
    list_display = ("nom",)


@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ("marque", "modele", "annee", "mode", "prix_affiche", "disponible")
    list_filter = ("mode", "motorisation", "marque", "disponible")
    search_fields = ("modele", "marque__nom")
    list_editable = ("disponible",)
