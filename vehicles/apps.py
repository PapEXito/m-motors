"""
déclare l'app "vehicles" pour django
django a besoin de cette AppConfig pour découvrir models, migrations et templates de l'app catalogue
réf dans INSTALLED_APPS config/settings.py
"""
from django.apps import AppConfig

# https://github.com/django/djangoproject.com/blob/main/checklists/apps.py

class VehiclesConfig(AppConfig):
    name = "vehicles"
