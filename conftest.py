"""
Configuration pytest partagée pour les trois applications.
pytest-django lit DJANGO_SETTINGS_MODULE depuis pytest.ini et initialise Django
avant de collecter les tests. Ce fichier peut accueillir des fixtures globales.
"""
import pytest


@pytest.fixture
def client():
    """Client HTTP Django réutilisé dans tous les tests (unit + fonctionnels)."""
    from django.test import Client
    return Client()
