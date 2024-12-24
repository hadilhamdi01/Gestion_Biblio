from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect 
from .views import delete_member
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    #path('', views.home, name='home'),  # Page d'accueil
    path('', lambda request: redirect('login')),
    path('login/', views.CustomLoginView.as_view(), name='login'),  
    path('logout/', views.custom_logout, name='logout'), 
    path('home/index/', views.home, name='home_index'), 
    path('home/adherents/', views.liste_adhérents, name='liste_adhérents'),  
    path('delete-member/<str:member_id>/', delete_member, name='delete_member'),
    path('edit-member/', edit_member, name='edit_member'),
    path('home/list_books/', views.list_books, name='list_books'), 
    path('authors/', views.authors_view, name='authors_view'), 




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
