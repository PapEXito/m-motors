"""

création de dossier achat/LLD + consult et changement de statut en admin only
c'est le coeur du flow "passer commande" du site sans ça aucune transac client
utilise dossiers/forms.py et dossiers/models.py vérifie vehicles/models.py.Vehicule rend templates/dossiers/
"""
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from vehicles.models import Vehicule
from .forms import DossierAchatForm, DossierLocationForm
from .models import DossierAchat, DossierLocation

# table de dispatch type → (form, model, libellé), comme ça une seule vue sert pour
# achat ET location ,ajouter un type = une ligne, pas de copier-coller de vue
TYPES = {
    "achat": (DossierAchatForm, DossierAchat, "Dossier d'achat"),
    "location": (DossierLocationForm, DossierLocation, "Dossier de location longue durée"),
}


# petit helper si le type url est inconnu on renvoie à Http404 c'est l'exception officielle Django.
# https://docs.djangoproject.com/en/6.0/topics/http/views/#the-http404-exception
def _resolve(type_dossier):
    if type_dossier not in TYPES:
        raise Http404
    return TYPES[type_dossier]


"""
on filtre directe sur disponible=True un véhicule indispo = 404,
plutôt que de laisser créer un dossier qui n'aurait jamais dû exister de base

`request.POST or None` même appel pour GET (form vide) et POST (form rempli)

commit=False pour pouvoir injecter client + véhicule depuis la session/url
avant de save.
https://docs.djangoproject.com/en/6.0/topics/forms/modelforms/#the-save-method
"""
@login_required
def creer_dossier(request, type_dossier, vehicule_id):
    form_class, _, titre = _resolve(type_dossier)
    vehicule = get_object_or_404(Vehicule, pk=vehicule_id, disponible=True)

    form = form_class(request.POST or None, request.FILES or None)
    if form.is_valid():
        dossier = form.save(commit=False)
        dossier.client = request.user
        dossier.vehicule = vehicule
        dossier.save()
        return redirect("accounts:dashboard")
    return render(request, "dossiers/create.html", {"form": form, "vehicule": vehicule, "titre": titre})


"""
client=request.user mis dans le filtre direct impossible de voir le dossier
de quelquun d'autre même en devinant l'id L'autorisation est dans la requête sql,
c'est plus safe qu'un if dossier.client != request.user d'après les doc django

"""
@login_required
def detail_dossier(request, type_dossier, pk):
    _, model, _ = _resolve(type_dossier)
    qs = model.objects.all() if request.user.is_staff else model.objects.filter(client=request.user)
    dossier = get_object_or_404(qs, pk=pk)
    # Admin uniquement : changement de statut via POST (PRG pour éviter le double-submit au refresh)
    if request.method == "POST" and request.user.is_staff:
        statut = request.POST.get("statut")
        if statut in model.StatutChoices.values:
            dossier.statut = statut
            dossier.save(update_fields=["statut"])
            return redirect(request.path)
    return render(request, "dossiers/detail.html", {"dossier": dossier, "type_dossier": type_dossier})
