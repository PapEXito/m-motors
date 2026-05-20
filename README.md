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
- pytest + pytest-django (tests unitaires + fonctionnels)

## Lancement local

**Option rapide (Windows) :** double-cliquer sur `start.bat` — crée le venv, installe les dépendances, migre, seed, ouvre le navigateur.

**Option manuelle :**

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

# Tests fonctionnels uniquement
python -m pytest tests_fonctionnels.py -v
```

## Comptes de test (autogen)

| Rôle   | Identifiant | Mot de passe |
|--------|-------------|--------------|
| Admin  | admin       | Admin123!    |
| Client | client      | Client123!   |

## Structure

```
config/         Settings, urls, wsgi
vehicles/       Modèles Marque + Vehicule, catalogue + commande seed_data
accounts/       Inscription, connexion, espace client + dashboard admin
dossiers/       Dossier achat ou LLD, upload des 4 pièces, workflow statut
templates/      HTML hérités de base.html
static/css/     Feuille de style unique (design tokens)
imgs/           Photos véhicules — imgs/<slug>/{1,2,3}.png
manage.py       Entrée CLI Django
requirements.txt
Procfile        Détection web Railway
railway.json    startCommand prod (migrate + seed + collectstatic + gunicorn)
.env.example    Template variables d'environnement
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

## Déploiement Railway

1. Push sur GitHub
2. Railway → New → Deploy from GitHub repo → sélectionner le repo
3. Railway → + Add → Database → Add PostgreSQL (génère `DATABASE_URL` automatiquement)
4. Variables → Raw Editor → ajouter les 4 autres variables (SECRET_KEY, DEBUG, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS)
5. Settings → Networking → Generate Domain
6. Deployments → Redeploy

Le `railway.json` chaîne `migrate → seed_data → collectstatic → gunicorn` à chaque démarrage.
La base PostgreSQL Railway est persistante entre les redeploys (contrairement à SQLite).
