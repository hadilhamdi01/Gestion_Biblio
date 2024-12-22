from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect  # Ajoutez cette importation pour la redirection

urlpatterns = [
    #path('', views.home, name='home'),  # Page d'accueil
    path('', lambda request: redirect('login')),
    path('login/', views.CustomLoginView.as_view(), name='login'),  # Connexion avec la vue personnalisée
    path('logout/', views.custom_logout, name='logout'),  # Déconnexion
    path('home/index/', views.home, name='home_index'), 
]
