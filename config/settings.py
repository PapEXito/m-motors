"""
config centrale Django apps installées, middleware, DB, statics, sécu prod
tout le comportement du framework auth, templates, WhiteNoise, ALLOWED_HOSTS c'est ici sans cette config rien ne tourne
lu par manage.py et wsgi.py au start, réf par toutes les app AUTH_USER_MODEL, STATIC_URL etc...
"""
import os
from pathlib import Path
import dj_database_url

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
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
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

# PostgreSQL en production (via DATABASE_URL injecté par Railway).
# SQLite uniquement en développement local si DATABASE_URL n'est pas défini.
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR}/db.sqlite3",
        conn_max_age=600,
    )
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
    # https://docs.djangoproject.com/en/5.0/topics/security/
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 an
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "same-origin"
    X_FRAME_OPTIONS = "DENY"

# Destinataires des alertes ERROR (handler mail_admins du LOGGING ci-dessous).
# Format env : "Nom1:mail1@x.fr,Nom2:mail2@x.fr"
ADMINS = [
    tuple(entry.split(":", 1))
    for entry in os.environ.get("DJANGO_ADMINS", "").split(",")
    if ":" in entry
]
SERVER_EMAIL = os.environ.get("SERVER_EMAIL", "alerts@m-motors.local")
EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"

# Surveillance : logs fichier + console + alerting mail_admins sur ERROR.
# https://docs.djangoproject.com/en/5.0/topics/logging/
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {"format": "[{asctime}] {levelname} {message}", "style": "{"},
    },
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file_app": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "app.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
        },
        "file_errors": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "errors.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "filters": ["require_debug_false"],
            "include_html": True,
        },
    },
    "root": {"handlers": ["console", "file_app"], "level": "INFO"},
    "loggers": {
        "django": {
            "handlers": ["console", "file_app"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["file_errors", "mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["file_errors", "mail_admins"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

# Sentry — alerting temps réel optionnel. Activé si SENTRY_DSN est défini.
# https://docs.sentry.io/platforms/python/integrations/django/
SENTRY_DSN = os.environ.get("SENTRY_DSN", "")
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=float(os.environ.get("SENTRY_TRACES_RATE", "0.1")),
        send_default_pii=False,
        environment=os.environ.get("SENTRY_ENV", "production"),
    )