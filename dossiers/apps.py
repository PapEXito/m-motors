"""

déclare l'app "dossiers" à Django
nécessaire pour que Django enregistre les models DossierAchat / DossierLocation et leurs migrations
réf dans INSTALLED_APPS config/settings.py
"""
from django.apps import AppConfig

class DossiersConfig(AppConfig):
    name = "dossiers"