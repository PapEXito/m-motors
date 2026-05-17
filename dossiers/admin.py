"""
enregistre DossierAchat et DossierLocation dans /admin/ avec filtre par statut
permet à admin de consulter et edit le statut d'un dossier directement depuis l'ui django
utilise dossiers/models.py accessible via /admin/ déclaré dans config/urls.py

"""
from django.contrib import admin
from .models import DossierAchat, DossierLocation

# https://github.com/django/djangoproject.com/blob/main/blog/admin.py

@admin.register(DossierAchat, DossierLocation)
class DossierAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "vehicule", "statut", "created_at")
    list_filter = ("statut",)
    list_editable = ("statut",)
