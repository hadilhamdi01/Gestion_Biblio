from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Nom d'utilisateur", max_length=255)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
