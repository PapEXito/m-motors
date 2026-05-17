"""
déclare l'app "accounts" à Django nécessaire pour que Django charge l'app auth custom inscription/dashboard
réf dans INSTALLED_APPS config/settings.py
"""
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    name = "accounts"