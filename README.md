# M-Motors

Application Django de vente et location longue durée (LLD) de véhicules d'occasion
- https://m-motors-production.up.railway.app/

## Stack

- Django 5 / Python 3.12+
- **PostgreSQL** (production via `DATABASE_URL`) · SQLite (développement local uniquement)
- `dj-database-url` — parsing de l'URL de connexion
- WhiteNoise (fichiers statiques)
- Gunicorn (serveur WSGI prod)
- Pillow (uploads images)
- psycopg2-binary (driver PostgreSQL)
- pytest + pytest-django (tests unitaires + fonctionnels)

## Lancement local

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

Site : http://127.0.0.1:8000 — Admin Django : `/admin/`

## Tests

```bash
# Tests unitaires + fonctionnels (28 tests au total)
python -m pytest -v

# Tests fonctionnels uniquement (parcours end-to-end)
python -m pytest tests_fonctionnels.py -v

# Tests unitaires d'une app
python -m pytest vehicles/tests.py -v
```

Configuration pytest : `pytest.ini` (settings = `config.settings`) + `conftest.py` (fixtures partagées).

## Comptes de test (autogen via `seed_data`)

| Rôle   | Identifiant | Mot de passe |
|--------|-------------|--------------|
| Admin  | admin       | Admin123!    |
| Client | client      | Client123!   |

La commande `seed_data` crée aussi 25 véhicules de démonstration (Audi, BMW, Peugeot, Renault, Volkswagen) avec leurs photos.

## Structure

```
config/                 Settings, urls, wsgi
vehicles/               Modèles Marque + Vehicule, catalogue
  └── management/commands/seed_data.py   Génère les 25 véhicules + 2 comptes
accounts/               Inscription, connexion, espace client + dashboard admin
dossiers/               Dossier achat ou LLD, upload des 4 pièces, workflow statut
templates/              HTML hérités de base.html (accounts/, dossiers/, vehicles/)
static/css/style.css    Feuille de style unique (design tokens)
imgs/                   Photos véhicules — imgs/<slug>/{1,2,3}.png
media/                  Uploads runtime (justificatifs dossiers, photos custom)
tests_fonctionnels.py   Tests end-to-end (parcours achat, LLD, admin)
conftest.py             Fixtures pytest partagées
pytest.ini              Config pytest-django
manage.py               Entrée CLI Django
requirements.txt        Dépendances Python
Procfile                Détection web Railway
railway.json            startCommand prod (migrate + seed + collectstatic + gunicorn)
.env.example            Template variables d'environnement
.gitignore              venv, __pycache__, db.sqlite3, media/, .env
start.bat               Bootstrap local Windows (venv + install + migrate + seed + run)
```

## Fonctionnalités

- Catalogue filtrable (marque, mode, motorisation, prix max, km max, modèle)
- Inscription / connexion / déconnexion
- Dossier d'achat (option reprise) ou location LLD (12/24/36/48 mois, assurance, entretien)
- Calcul automatique du loyer mensuel (+30 € assurance, +25 € entretien)
- Upload de 4 pièces justificatives (CNI, domicile, RIB, revenus), 5 Mo max, PDF/JPG/PNG
- Workflow statut : déposé → en traitement → validé / refusé
- Espace client : liste des dossiers + pastilles de statut
- Dashboard admin (`is_staff`) : voit tous les dossiers, change le statut en 1 clic

## Variables d'environnement

Voir `.env.example`. En prod (5 variables obligatoires) :

```
SECRET_KEY=<clé aléatoire 50+ caractères>
DEBUG=False
ALLOWED_HOSTS=.railway.app
CSRF_TRUSTED_ORIGINS=https://*.railway.app
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

En local, aucune variable n'est requise : `SECRET_KEY` retombe sur une clé dev, `DEBUG=True` par défaut, `DATABASE_URL` non défini = SQLite (`db.sqlite3`).

En prod (`DEBUG=False`), les cookies session/CSRF passent en `Secure` et `SECURE_PROXY_SSL_HEADER` est activé pour le proxy HTTPS Railway.

## Déploiement Railway

1. Push sur GitHub
2. Railway → New → Deploy from GitHub repo → sélectionner le repo
3. Railway → + Add → Database → Add PostgreSQL (génère `DATABASE_URL` automatiquement)
4. Variables → Raw Editor → ajouter les 4 autres variables (SECRET_KEY, DEBUG, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS)
5. Settings → Networking → Generate Domain
6. Deployments → Redeploy

Le `railway.json` chaîne `migrate → seed_data → collectstatic → gunicorn` à chaque démarrage (builder RAILPACK, restart `ON_FAILURE` × 3).
La base PostgreSQL Railway est persistante entre les redeploys (contrairement à SQLite).

## Branches

- `main` — branche stable, déployée sur Railway
- `develop` — intégration des features
- `feature/postgresql` — migration SQLite → PostgreSQL + `dj-database-url`
- `feature/tests-fonctionnels` — suite de tests end-to-end + outillage dev
