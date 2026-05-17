"""
tests pytest de la création de dossier validation taille fichier calcul loyer_total avec option
verrouille le flow client critique upload doc choix options LLD et  loyer
utilise dossiers/models.py et vehicles/models.py simule les upload avec SimpleUploadedFile
"""
import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from dossiers.models import DossierAchat, DossierLocation
from vehicles.models import Marque, Vehicule


@pytest.fixture
def user(db):
    return User.objects.create_user(username="alice", password="Strong123!")


@pytest.fixture
def vehicule_achat(db):
    marque = Marque.objects.create(nom="Peugeot")
    return Vehicule.objects.create(
        marque=marque, modele="208", annee=2022, kilometrage=15000,
        motorisation="essence", mode="achat", prix_vente=Decimal("15990"),
    )


@pytest.fixture
def vehicule_location(db):
    marque = Marque.objects.create(nom="Renault")
    return Vehicule.objects.create(
        marque=marque, modele="Zoe", annee=2023, kilometrage=8000,
        motorisation="electrique", mode="location", loyer_mensuel=Decimal("269"),
    )


def _doc(name="cni.pdf"):
    return SimpleUploadedFile(name, b"%PDF-1.4 fake", content_type="application/pdf")


def _docs():
    return {"cni": _doc(), "justificatif_domicile": _doc(), "rib": _doc(), "justificatif_revenus": _doc()}


def test_creation_dossier_achat(client, user, vehicule_achat):
    client.login(username="alice", password="Strong123!")
    response = client.post(reverse("dossiers:create", args=["achat", vehicule_achat.id]),
                           {"reprise_vehicule": "on", **_docs()})
    assert response.status_code == 302
    assert DossierAchat.objects.filter(client=user).exists()


def test_creation_dossier_location(client, user, vehicule_location):
    client.login(username="alice", password="Strong123!")
    response = client.post(reverse("dossiers:create", args=["location", vehicule_location.id]),
                           {"duree_mois": 24, "assurance": "on", **_docs()})
    assert response.status_code == 302
    dossier = DossierLocation.objects.get(client=user)
    assert dossier.duree_mois == 24 and dossier.assurance


def test_fichier_trop_gros_rejete(client, user, vehicule_achat):
    client.login(username="alice", password="Strong123!")
    big = SimpleUploadedFile("big.pdf", b"x" * (6 * 1024 * 1024), content_type="application/pdf")
    response = client.post(reverse("dossiers:create", args=["achat", vehicule_achat.id]),
                           {**_docs(), "cni": big})
    assert response.status_code == 200
    assert "cni" in response.context["form"].errors


def test_creation_requiert_authentification(client, vehicule_achat):
    response = client.get(reverse("dossiers:create", args=["achat", vehicule_achat.id]))
    assert response.status_code == 302


def test_loyer_total_avec_options(user, vehicule_location):
    dossier = DossierLocation.objects.create(
        client=user, vehicule=vehicule_location, duree_mois=24,
        assurance=True, entretien=True,
        cni=_doc(), justificatif_domicile=_doc(), rib=_doc(), justificatif_revenus=_doc(),
    )
    assert dossier.loyer_total == 269 + 30 + 25