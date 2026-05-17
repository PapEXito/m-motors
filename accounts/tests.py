"""
tests pytest de auth/inscription/connexion accès dashboard restreint
verrouille les flows critiques d'auth toute régression bloquerait l'accès au site
utilise les url de accounts/urls.py et User natif Django
"""
import pytest
from django.contrib.auth.models import User
from django.urls import reverse

# https://github.com/django/djangoproject.com/blob/main/accounts/tests.py

@pytest.fixture
def user(db):
    return User.objects.create_user(username="alice", password="Strong123!")


def test_inscription_cree_un_user(client, db):
    response = client.post(reverse("accounts:register"), {
        "username": "bob", "email": "bob@example.com",
        "password1": "MotDePasseFort1!", "password2": "MotDePasseFort1!",
    })
    assert response.status_code == 302
    assert User.objects.filter(username="bob").exists()


def test_connexion_valide(client, user):
    response = client.post(reverse("accounts:login"), {"username": "alice", "password": "Strong123!"})
    assert response.status_code == 302


def test_dashboard_protege(client, db):
    response = client.get(reverse("accounts:dashboard"))
    assert response.status_code == 302  # redirige vers login


def test_dashboard_accessible_si_connecte(client, user):
    client.login(username="alice", password="Strong123!")
    assert client.get(reverse("accounts:dashboard")).status_code == 200