from django.contrib.auth import logout
from django.shortcuts import render  # Ajoutez cette ligne

from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm

# Vue de la page d'accueil
def home(request):
    return render(request, 'home/index.html')

# Déconnexion de l'utilisateur
def custom_logout(request):
    logout(request)  # Déconnecte l'utilisateur
    return redirect('login')  # Redirige vers la page de connexion après déconnexion

# Vue personnalisée pour la connexion
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'  # Chemin vers votre template de connexion
    authentication_form = CustomLoginForm  # Formulaire personnalisé pour la connexion
