"""
point d'entrée CLI de Django runserver, migrate, createsuperuser, seed_data etc...
sans ce fichier aucune commande `python manage.py ...` ne fonctionne donc impossible de lancer/migrer/admin le projet
lit config/settings.py via DJANGO_SETTINGS_MODULE dispatch vers les commandes des apps vehicles, accounts, dossiers

"""
import os
import sys

def main():
    #Run admin task
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django, Maybe not installed"
            "avalable on your PYTHONPATH env var ?"
            "forget to activate your env ?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()