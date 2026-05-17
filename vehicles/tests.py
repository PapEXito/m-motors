"""
tests pytest du catalogue validation du __str__, du prix_affiche, des filtres et de la vue
garantit que les filtres et l'affichage prix achat/location ne régressent pas en cas de modif
utilise vehicles/models.py et les url de vehicles/urls.py lancé via `pytest`
"""
import pytest
from decimal import Decimal
from django.urls import reverse
from vehicles.models import Marque, Vehicule

@pytest.fixture
def marque(db):
    return Marque.objects.create(nom="Peugeot")


@pytest.fixture
def vehicule_achat(marque):
    return Vehicule.objects.create(
        marque=marque, modele="208", annee=2022, kilometrage=15000,
        motorisation="essence", mode="achat", prix_vente=Decimal("15990"),
    )


@pytest.fixture
def vehicule_location(marque):
    return Vehicule.objects.create(
        marque=marque, modele="e-208", annee=2023, kilometrage=8000,
        motorisation="electrique", mode="location", loyer_mensuel=Decimal("299"),
    )


def test_str_vehicule(vehicule_achat):
    assert str(vehicule_achat) == "Peugeot 208 (2022)"


def test_prix_affiche(vehicule_achat, vehicule_location):
    assert "€" in vehicule_achat.prix_affiche
    assert "mois" in vehicule_location.prix_affiche


def test_recherche_par_mode(client, vehicule_achat, vehicule_location):
    response = client.get(reverse("vehicles:search"), {"mode": "achat"})
    vehicules = list(response.context["vehicules"])
    assert vehicule_achat in vehicules and vehicule_location not in vehicules


def test_filtre_prix_max_exclut(client, vehicule_achat):
    response = client.get(reverse("vehicles:search"), {"prix_max": "10000"})
    assert vehicule_achat not in response.context["vehicules"]


def test_recherche_modele(client, vehicule_achat):
    response = client.get(reverse("vehicles:search"), {"q": "208"})
    assert vehicule_achat in response.context["vehicules"]


def test_detail_vehicule(client, vehicule_achat):
    response = client.get(reverse("vehicles:detail", args=[vehicule_achat.pk]))
    assert response.status_code == 200