from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect

# Create your views here.

def home(request):
    return render(request,'home/index.html')

#def login_view(request):
    #return render(request, 'accounts/login.html')
#def register_view(request):
    #return render(request, 'accounts/register.html')

def custom_logout(request):
    logout(request)  # Déconnecte l'utilisateur
    return redirect('/')  

