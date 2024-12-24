from django.contrib.auth import logout
from django.shortcuts import render  # Ajoutez cette ligne
from .models import Adherent
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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


def liste_adhérents(request):
    if request.method == "POST":
        # Récupération des données du formulaire
        nom_adh = request.POST.get("nom_adh")
        nbr_emprunts_adh = request.POST.get("nbr_emprunts_adh")

        # Création d'un nouvel adhérent
        if nom_adh and nbr_emprunts_adh:
            Adherent.objects.create(
                nom_adh=nom_adh,
                nbr_emprunts_adh=int(nbr_emprunts_adh)
            )
            return redirect("liste_adhérents")
    adherents = Adherent.objects.all().order_by('nom_adh')
    return render(request, 'home/adherents.html', {'adherents': adherents})


@csrf_exempt
def delete_member(request, member_id):
    if request.method == 'POST':
        try:
            member = Adherent.objects.get(code_adh=member_id)
            member.delete()
            return JsonResponse({'success': True})
        except Adherent.DoesNotExist:
            return JsonResponse({'error': 'Member not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
def edit_member(request):
    if request.method == 'POST':
        try:
            member_id = request.POST.get('code_adh')
            name = request.POST.get('nom_adh')
            loans = request.POST.get('nbr_emprunts_adh')

            member = Adherent.objects.get(code_adh=member_id)
            member.nom_adh = name
            member.nbr_emprunts_adh = loans
            member.save()

            return JsonResponse({'success': True})
        except Adherent.DoesNotExist:
            return JsonResponse({'error': 'Member not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

