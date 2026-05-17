"""
logique du catalogue, filtrage des véhicules par marque/prix/km/motorisation vue détail
c'est le coeur de la partie "consultation" du site ce que voient les visiteurs avant d'acheter/louer
lit vehicles/models.py rend templates/vehicles/search.html et detail.html routée via vehicles/urls.py
"""
from django.shortcuts import get_object_or_404, render
from .models import Marque, Vehicule

# https://github.com/django/djangoproject.com/blob/main/checklists/views.py

"""
mapping param GET = lookup ORM comme ça plus besoin des if elif
pour ajouter un filtre une ligne tout ici et c'est plié
https://docs.djangoproject.com/en/6.0/ref/models/querysets/#field-lookups
"""

FILTERS = {
    "marque": "marque_id",
    "mode": "mode",
    "motorisation": "motorisation",
    "prix_max": "prix_vente__lte",
    "km_max": "kilometrage__lte",
    "q": "modele__icontains",
}

"""
select_related pour éviter le n+1  un seul JOIN au lieu de 25 requêtes
vu que chaque carte affiche la marque
https://docs.djangoproject.com/en/6.0/ref/models/querysets/#select-related
"""
def catalogue(request):

    qs = Vehicule.objects.filter(disponible=True).select_related("marque")

    for param, field in FILTERS.items():
        if value := request.GET.get(param):
            qs = qs.filter(**{field: value})
    return render(request, "vehicles/search.html", {
        "vehicules": qs,
        "marques": Marque.objects.all(),
        "motorisations": Vehicule.MotorisationChoices.choices,
        "modes": Vehicule.ModeChoices.choices,
        "params": request.GET,
    })


def vehicule_detail(request, pk):
    return render(request, "vehicles/detail.html", {
        "vehicule": get_object_or_404(Vehicule, pk=pk),
    })
