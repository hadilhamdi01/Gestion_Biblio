from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Livre, Auteur

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Nom d'utilisateur", max_length=255)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = ['titre_livre', 'nbre_page', 'auteur', 'image', 'disponibilite']

class AuteurForm(forms.ModelForm):
    class Meta:
        model = Auteur
        fields = ['nom_auteur', 'prenom_auteur']
