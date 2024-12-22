from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('',views.home,name='index'),
    #path('', views.login_view, name='login'),  
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    #path('', auth_views.LoginView.as_view(template_name='accounts/login.html')), 
    #path('register/', views.register_view, name='register'),
    #path('', views.home, name='index'),
    path('logout/', views.custom_logout, name='logout'),
    
]
