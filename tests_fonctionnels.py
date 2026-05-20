"""
Tests fonctionnels bout-en-bout — reproduisent des scénarios utilisateur complets.
Contrairement aux tests unitaires qui testent chaque fonction isolément,
ces tests simulent un vrai parcours : inscription → catalogue → dossier → dashboard.
Lancés avec : python -m pytest tests_fonctionnels.py -v
"""
import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from dossiers.models import DossierAchat, DossierLocation
from vehicles.models import Marque, Vehicule


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _docs():
    """Génère les 4 pièces justificatives PDF minimales requises pour un dossier."""
    f = lambda n: SimpleUploadedFile(n, b"%PDF-1.4 fake", content_type="application/pdf")
    return {
        "cni": f("cni.pdf"),
        "justificatif_domicile": f("domicile.pdf"),
        "rib": f("rib.pdf"),
        "justificatif_revenus": f("revenus.pdf"),
    }


# ─── Fixtures partagées ───────────────────────────────────────────────────────

@pytest.fixture
def marque(db):
    return Marque.objects.create(nom="Renault")


@pytest.fixture
def vehicule_achat(marque):
    return Vehicule.objects.create(
        marque=marque, modele="Clio V", annee=2022, kilometrage=20000,
        motorisation="essence", mode="achat", prix_vente=Decimal("15990"),
    )


@pytest.fixture
def vehicule_location(marque):
    return Vehicule.objects.create(
        marque=marque, modele="Zoe", annee=2023, kilometrage=5000,
        motorisation="electrique", mode="location", loyer_mensuel=Decimal("299"),
    )


# ─── Scénario 1 : Accès public ───────────────────────────────────────────────

def test_home_accessible_sans_connexion(client):
    """La page d'accueil est publique — aucune connexion requise."""
    assert client.get(reverse("home")).status_code == 200


def test_catalogue_accessible_et_affiche_vehicules(client, vehicule_achat):
    """Le catalogue est public et retourne les véhicules disponibles."""
    response = client.get(reverse("vehicles:search"))
    assert response.status_code == 200
    assert vehicule_achat in response.context["vehicules"]


def test_fiche_vehicule_accessible_sans_connexion(client, vehicule_achat):
    """La fiche détail d'un véhicule est accessible sans être connecté."""
    response = client.get(reverse("vehicles:detail", args=[vehicule_achat.pk]))
    assert response.status_code == 200
    assert response.context["vehicule"] == vehicule_achat


# ─── Scénario 2 : Inscription et auto-connexion ──────────────────────────────

def test_inscription_cree_compte_et_ouvre_session(client, db):
    """L'inscription crée le compte et connecte automatiquement l'utilisateur."""
    response = client.post(reverse("accounts:register"), {
        "username": "nouveau", "email": "nouveau@test.fr",
        "password1": "MotDePasseF0rt!", "password2": "MotDePasseF0rt!",
    })
    assert response.status_code == 302
    assert "_auth_user_id" in client.session
    assert User.objects.filter(username="nouveau").exists()


def test_inscription_redirige_vers_dashboard(client, db):
    """Après inscription, l'utilisateur arrive directement sur son dashboard."""
    response = client.post(reverse("accounts:register"), {
        "username": "nouveau2", "email": "nouveau2@test.fr",
        "password1": "MotDePasseF0rt!", "password2": "MotDePasseF0rt!",
    }, follow=True)
    assert response.redirect_chain[-1][0] == reverse("accounts:dashboard")


# ─── Scénario 3 : Parcours achat complet ─────────────────────────────────────

def test_parcours_achat_complet(client, vehicule_achat, db):
    """Scénario bout-en-bout : connexion → catalogue → fiche → dossier achat → dashboard."""
    user = User.objects.create_user("alice", "alice@test.fr", "Fort2024!")
    client.login(username="alice", password="Fort2024!")

    # Consultation catalogue
    assert client.get(reverse("vehicles:search")).status_code == 200

    # Fiche véhicule
    assert client.get(reverse("vehicles:detail", args=[vehicule_achat.pk])).status_code == 200

    # Dépôt dossier d'achat
    response = client.post(
        reverse("dossiers:create", args=["achat", vehicule_achat.pk]),
        {"reprise_vehicule": "on", **_docs()},
    )
    assert response.status_code == 302
    assert DossierAchat.objects.filter(client=user).exists()

    # Dashboard affiche le dossier créé
    dash = client.get(reverse("accounts:dashboard"))
    assert DossierAchat.objects.get(client=user) in dash.context["dossiers_achat"]


# ─── Scénario 4 : Parcours location LLD ──────────────────────────────────────

def test_parcours_location_avec_options(client, vehicule_location, db):
    """Scénario location LLD : dépôt avec assurance + entretien, vérification loyer total."""
    user = User.objects.create_user("bob", "bob@test.fr", "Fort2024!")
    client.login(username="bob", password="Fort2024!")

    client.post(
        reverse("dossiers:create", args=["location", vehicule_location.pk]),
        {"duree_mois": 24, "assurance": "on", "entretien": "on", **_docs()},
    )

    dossier = DossierLocation.objects.get(client=user)
    assert dossier.duree_mois == 24
    assert dossier.assurance and dossier.entretien
    assert dossier.loyer_total == float(vehicule_location.loyer_mensuel) + 30 + 25


def test_detail_dossier_location_accessible(client, vehicule_location, db):
    """Le client peut consulter la fiche détail de son dossier de location."""
    user = User.objects.create_user("carol", "carol@test.fr", "Fort2024!")
    client.login(username="carol", password="Fort2024!")
    client.post(
        reverse("dossiers:create", args=["location", vehicule_location.pk]),
        {"duree_mois": 12, **_docs()},
    )
    dossier = DossierLocation.objects.get(client=user)
    response = client.get(reverse("dossiers:detail", args=["location", dossier.pk]))
    assert response.status_code == 200


# ─── Scénario 5 : Contrôle d'accès ───────────────────────────────────────────

def test_dashboard_redirige_si_non_connecte(client, db):
    """Un visiteur non connecté tentant d'accéder au dashboard est redirigé vers login."""
    response = client.get(reverse("accounts:dashboard"))
    assert response.status_code == 302
    assert "connexion" in response["Location"]


def test_creation_dossier_exige_connexion(client, vehicule_achat):
    """Créer un dossier sans être connecté redirige vers la page de connexion."""
    response = client.get(reverse("dossiers:create", args=["achat", vehicule_achat.pk]))
    assert response.status_code == 302


def test_client_ne_peut_pas_voir_dossier_dautrui(client, vehicule_achat, db):
    """Un client ne peut pas accéder au dossier d'un autre client : retour 404."""
    proprietaire = User.objects.create_user("proprio", "p@test.fr", "Fort2024!")
    intrus = User.objects.create_user("intrus", "i@test.fr", "Fort2024!")

    client.login(username="proprio", password="Fort2024!")
    client.post(
        reverse("dossiers:create", args=["achat", vehicule_achat.pk]),
        {"reprise_vehicule": "on", **_docs()},
    )
    dossier = DossierAchat.objects.get(client=proprietaire)

    client.logout()
    client.login(username="intrus", password="Fort2024!")
    assert client.get(reverse("dossiers:detail", args=["achat", dossier.pk])).status_code == 404


# ─── Scénario 6 : Workflow admin ─────────────────────────────────────────────

def test_admin_valide_un_dossier_client(client, vehicule_achat, db):
    """L'admin peut changer le statut d'un dossier de 'déposé' à 'validé'."""
    client_user = User.objects.create_user("client_s", "cs@test.fr", "Fort2024!")
    User.objects.create_superuser("admin_s", "as@test.fr", "Admin2024!")

    client.login(username="client_s", password="Fort2024!")
    client.post(
        reverse("dossiers:create", args=["achat", vehicule_achat.pk]),
        {"reprise_vehicule": "on", **_docs()},
    )
    dossier = DossierAchat.objects.get(client=client_user)
    assert dossier.statut == "depose"

    client.logout()
    client.login(username="admin_s", password="Admin2024!")
    client.post(reverse("dossiers:detail", args=["achat", dossier.pk]), {"statut": "valide"})
    dossier.refresh_from_db()
    assert dossier.statut == "valide"


def test_admin_voit_tous_les_dossiers_dans_dashboard(client, vehicule_achat, db):
    """L'admin voit les dossiers de tous les clients sur son dashboard."""
    client_user = User.objects.create_user("client_v", "cv@test.fr", "Fort2024!")
    User.objects.create_superuser("admin_v", "av@test.fr", "Admin2024!")

    client.login(username="client_v", password="Fort2024!")
    client.post(
        reverse("dossiers:create", args=["achat", vehicule_achat.pk]),
        {"reprise_vehicule": "on", **_docs()},
    )

    client.logout()
    client.login(username="admin_v", password="Admin2024!")
    response = client.get(reverse("accounts:dashboard"))
    dossier = DossierAchat.objects.get(client=client_user)
    assert dossier in response.context["dossiers_achat"]
