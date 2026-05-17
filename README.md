# M-Motors

Application Django de vente et location longue durée (LLD) de véhicules d'occasion
- https://m-motors-production.up.railway.app/

## Stack

- Django 5 / Python 3.12+
- SQLite (zéro config)
- WhiteNoise (fichiers statiques)
- Gunicorn (serveur WSGI prod)
- Pillow (uploads images)

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

Voir `.env.example`. En prod :

```
SECRET_KEY=<clé aléatoire 50+ caractères>
DEBUG=False
ALLOWED_HOSTS=.railway.app
CSRF_TRUSTED_ORIGINS=https://*.railway.app
```

## Déploiement Railway

1. Push sur GitHub
2. Railway → New → Deploy from GitHub repo → sélectionner le repo
3. Variables → Raw Editor → coller les 4 variables ci-dessus
4. Settings → Networking → Generate Domain
5. Deployments → Redeploy

Le `railway.json` chaîne `migrate → seed_data → collectstatic → gunicorn` à chaque démarrage

## Notes

- Le filesystem Railway est éphémère : SQLite est wipée à chaque redeploy, le seed réinjecte la démo à chaque démarrage
- Pour de la persistance réelle, brancher PostgreSQL via `DATABASE_URL` + `dj-database-url`
