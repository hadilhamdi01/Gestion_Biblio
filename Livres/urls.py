from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect 
from .views import delete_member


urlpatterns = [
    #path('', views.home, name='home'),  # Page d'accueil
    path('', lambda request: redirect('login')),
    path('login/', views.CustomLoginView.as_view(), name='login'),  
    path('logout/', views.custom_logout, name='logout'), 
    path('home/index/', views.home, name='home_index'), 
    path('home/adherents/', views.liste_adhérents, name='liste_adhérents'),  
    path('delete-member/<str:member_id>/', delete_member, name='delete_member'),
    path('edit-member/', edit_member, name='edit_member'),



]
