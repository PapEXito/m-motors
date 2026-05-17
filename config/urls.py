"""
routeur racine, mappe chaque url du site vers l'app concernée vehicles, accounts, dossiers ou admin
sans ce fichier Django ne sait pas quelle view appeler quand un user visite une url
include() les urls.py de chaque app expose la home via templates/home.html sert media/ en dev
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("vehicules/", include("vehicles.urls")),
    path("compte/", include("accounts.urls")),
    path("dossiers/", include("dossiers.urls")),
]

"""
django gère les upload /media/ qu'en dev, en prod c'est whitenoise/railway qui gérent
de toute façon `static()` renvoie [] hors DEBUG, donc le `if` est juste une sécu
https://docs.djangoproject.com/en/6.0/howto/static-files/#serving-files-uploaded-by-a-user-during-development
"""

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)