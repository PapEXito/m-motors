"""
expose l'app Django sous forme d'objet WSGI
c'est ce que gunicorn sur Railway importe pour servir le site en prod via gunicorn config.wsgi
charge config/settings.py sert d'entrée http qui passe ensuite par config/urls.py
"""
import os
from django.core.wsgi import get_wsgi_application

# https://github.com/django/djangoproject.com/blob/main/djangoproject/wsgi.py

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
