"""
routes de l'app vehicles, /vehicules/ catalogue et /vehicules/<id>/ fiche détail
sépare le routage par app plus maintenable qu'un gros urls.py central
inclus par config/urls.py sous le préfixe vehicules/ pointe sur vehicles/views.py

"""
from django.urls import path
from . import views

# https://github.com/django/djangoproject.com/blob/main/checklists/urls.py

app_name = "vehicles"

urlpatterns = [
    path("", views.catalogue, name="search"),
    path("<int:pk>/", views.vehicule_detail, name="detail"),
]
