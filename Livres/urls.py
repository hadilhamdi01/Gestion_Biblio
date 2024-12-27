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
    path('book/<int:code_livre>/', views.book_detail, name='book_detail'),
    path('book/update/<int:code_livre>/', views.book_update, name='book_update'),
    path('book/delete/<int:code_livre>/', views.book_delete, name='book_delete'),
    path('edit-author/', edit_author, name='edit_author'),
    path('home/emprunt/', views.emprunt, name='emprunt'), 
    path('creer_emprunt/', views.creer_emprunt, name='creer_emprunt'),
    path('detail_emprunt/', views.detail_emprunt, name='detail_emprunt'),






]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
