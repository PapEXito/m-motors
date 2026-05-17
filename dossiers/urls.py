"""
routes /dossiers/ création et consultation d'un dossier achat/loc
permet au client de déposer un dossier après avoir choisi un véhicule du catalogue
inclu par config/urls.py sous le préfixe dossiers/ pointe sur dossiers/views.py

"""
from django.urls import path
from . import views

# https://github.com/django/djangoproject.com/blob/main/blog/urls.py

app_name = "dossiers"

urlpatterns = [
    path("creer/<str:type_dossier>/<int:vehicule_id>/", views.creer_dossier, name="create"),
    path("<str:type_dossier>/<int:pk>/", views.detail_dossier, name="detail"),
]