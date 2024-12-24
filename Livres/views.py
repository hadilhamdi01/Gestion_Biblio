from django.contrib.auth import logout
from django.shortcuts import render  
from .models import Adherent
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Livre, Auteur
from .forms import LivreForm, AuteurForm

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


# Liste des livres
def list_books(request):
      if request.method == "POST":
        titre_livre = request.POST.get('titre_livre')
        code_auteur = request.POST.get('auteur')  # Récupère l'auteur sélectionné
        nbre_page = request.POST.get('nbre_page')
        prix = request.POST.get('prix')
        disponibilite= request.POST.get('disponibilite')
        image = request.FILES.get('image')  # Récupère le fichier image

        # Vérifiez si l'auteur existe dans la base de données
        auteur = Auteur.objects.get(code_auteur=code_auteur)

        # Créez un nouveau livre
        Livre.objects.create(
            titre_livre=titre_livre,
            auteur=auteur,
            nbre_page=nbre_page,
            prix=prix,
            image=image,
           # disponibilite=disponibilite,
        )
        return redirect('list_books')  # Redirigez après la soumission du formulaire

      auteurs = Auteur.objects.all()  # Récupère tous les auteurs pour l'affichage
      print(auteurs)
      livres = Livre.objects.all()  # Optionnel : Récupérez les livres pour les afficher
   
      return render(request, 'home/list_books.html', {'livres': livres, 'auteurs': auteurs})



def authors_view(request):
    if request.method == "POST":
        nom_auteur = request.POST.get('nom_auteur')
        prenom_auteur = request.POST.get('prenom_auteur')
        
        # Création de l'auteur
        Auteur.objects.create(nom_auteur=nom_auteur, prenom_auteur=prenom_auteur)
        return redirect('authors_view')  # Redirigez vers la même page après l'ajout

    auteurs = Auteur.objects.all()  # Récupérez les auteurs pour les afficher
    return render(request, 'home/authors.html', {'auteurs': auteurs})

