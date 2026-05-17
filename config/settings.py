"""
config centrale Django apps installées, middleware, DB, statics, sécu prod
tout le comportement du framework auth, templates, WhiteNoise, ALLOWED_HOSTS c'est ici sans cette config rien ne tourne
lu par manage.py et wsgi.py au start, réf par toutes les app AUTH_USER_MODEL, STATIC_URL etc...
"""
import os
from pathlib import Path

# https://github.com/django/djangoproject.com/tree/main/djangoproject/settings

BASE_DIR = Path(__file__).resolve().parent.parent
"""
tout ce qui bouge entre dev/prod passe par des var env
la key "dev-insecure" sert en local, en vrai Railway injecte la bonne
https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/#secret-key
"""


"""
sans ça les POST crossorigin sont bloqués par le proxy HTTPS de Railway
https://docs.djangoproject.com/en/6.0/ref/settings/#csrf-trusted-origins
"""
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-insecure-key-change-me")
DEBUG = os.environ.get("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")
CSRF_TRUSTED_ORIGINS = os.environ.get(
    "CSRF_TRUSTED_ORIGINS", "https://*.railway.app"
).split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "vehicles",
    "accounts",
    "dossiers",
]

"""
whitenoise va juste après securitymiddleware c'est l'ordre de la doc
https://whitenoise.readthedocs.io/en/stable/django.html#enable-whitenoise
"""
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True


"""
# Le tuple (prefix, path) sert à exposer /imgs/ à part sans le mix au CSS/JS
# comme ça pas besoin de copier les photos dans static/
# https://docs.djangoproject.com/en/6.0/ref/settings/#staticfiles-dirs
"""
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static", ("imgs", BASE_DIR / "imgs")]
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "accounts:dashboard"
LOGOUT_REDIRECT_URL = "home"

DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024

# cookies sécurisés en prod sinon en dev sur http local ça casse la session
# railway met bien le header XForwardedProto donc on peut s'y fier
# https://docs.djangoproject.com/en/6.0/ref/settings/#secure-proxy-ssl-header
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True