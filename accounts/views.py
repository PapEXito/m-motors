"""
vue inscription création + autolog et dashboard liste des dossiers du user ou tous si admin
sans inscription pas de client sans dashboard pas de suivi de dossier
utilise accounts/forms.py lit dossiers/models.py pour afficher les dossiers rend les templates accounts/
"""
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from dossiers.models import DossierAchat, DossierLocation
from .forms import InscriptionForm

# https://github.com/django/djangoproject.com/blob/main/accounts/views.py

"""
login() direct après save() pour pas demander au client de retaper ses id juste apres s'être inscrit
https://docs.djangoproject.com/en/6.0/topics/auth/default/#django.contrib.auth.login
"""
def inscription(request):
    form = InscriptionForm(request.POST or None)
    if form.is_valid():
        user = form.save()

        login(request, user)
        return redirect("accounts:dashboard")
    return render(request, "accounts/register.html", {"form": form})

"""
select_related("vehicule__marque") = double JOIN en une seule requête.
Sans ça on aurait un n+1 sur le dashboard (1 query par ligne pour la marque)
https://docs.djangoproject.com/en/6.0/ref/models/querysets/#select-related
"""
@login_required
def dashboard(request):
    user = request.user
    # Admin voit tous les dossiers à traiter, un client ne voit que les siens
    achat = DossierAchat.objects.select_related("vehicule__marque")
    location = DossierLocation.objects.select_related("vehicule__marque")
    if not user.is_staff:
        achat = achat.filter(client=user)
        location = location.filter(client=user)
    return render(request, "accounts/dashboard.html", {
        "dossiers_achat": achat,
        "dossiers_location": location,
    })
