"""
routes /compte/ inscription, connexion, déconnexion, dashboard
centralise les url liées à auth réutilise les views Django LoginLogoutview
inclus par config/urls.py sous le préfixe compte/ pointe sur accounts/views.py et django.contrib.auth.views
"""
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

# https://github.com/django/djangoproject.com/blob/main/accounts/urls.py

app_name = "accounts"

"""
on utilise LoginView et LogoutView natif plutôt que de tout refaire à la main
https://docs.djangoproject.com/en/6.0/topics/auth/default/#using-the-views
"""

urlpatterns = [
    path("inscription/", views.inscription, name="register"),
    path("connexion/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("deconnexion/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
