"""
formulaire d'inscription qui étend usercreationform avec mail obligatoire et unique
qjango de base ne valide pas l'unicité des mail on l'ajoute ici pour éviter les doublons
utilisé par accounts/views.py vue inscription
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# https://github.com/django/djangoproject.com/blob/main/accounts/forms.py

"""
on utilise usercreationform tout est déjà prêt
https://docs.djangoproject.com/en/6.0/topics/auth/default/#top
"""

class InscriptionForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    """
        clean_<champ> c'est le hook Django pour valider un champ ici on bloque les mail
        déjà pris car le User natif de django.contrib.auth.models ne le fait en auto
        .exists() est plus simple que .get()+try/except.
         https://docs.djangoproject.com/en/6.0/ref/forms/validation/#form-and-field
    """

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Un compte existe déjà avec cet email.")
        return email