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
from .models import Livre, Auteur, Emprunt
from .forms import LivreForm, AuteurForm
from datetime import timedelta, datetime, date
from django.utils.timezone import now



# Vue de la page d'accueil
def home(request):
    return render(request, 'home/index.html')

# Déconnexion de l'utilisateur
def custom_logout(request):
    logout(request) 
    return redirect('login')  

# Vue personnalisée pour la connexion
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'  
    authentication_form = CustomLoginForm  


def liste_adhérents(request):
    if request.method == "POST":
        nom_adh = request.POST.get("nom_adh")
        nbr_emprunts_adh = request.POST.get("nbr_emprunts_adh")
        image = request.FILES.get('image')

        #if nom_adh and nbr_emprunts_adh and image:
        
        adherent = Adherent.objects.create(
                nom_adh=nom_adh,
                nbr_emprunts_adh=int(nbr_emprunts_adh),
                image=image
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
            image = request.FILES.get('image')

            member = Adherent.objects.get(code_adh=member_id)
            member.nom_adh = name
            member.nbr_emprunts_adh = loans
            member.image=image
            member.save()

            return JsonResponse({'success': True})
        except Adherent.DoesNotExist:
            return JsonResponse({'error': 'Member not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)


""" # Liste des livres
def list_books(request):
      if request.method == "POST":
        titre_livre = request.POST.get('titre_livre')
        code_auteur = request.POST.get('auteur') 
        nbre_page = request.POST.get('nbre_page')
        prix = request.POST.get('prix')
        disponibilite= request.POST.get('disponibilite')
        image = request.FILES.get('image') 
        auteur = Auteur.objects.get(code_auteur=code_auteur)
        Livre.objects.create(
            titre_livre=titre_livre,
            auteur=auteur,
            nbre_page=nbre_page,
            prix=prix,
            image=image,
           # disponibilite=disponibilite,
        )
        return redirect('list_books')  

      auteurs = Auteur.objects.all()  
      print(auteurs)
      livres = Livre.objects.all()  
   
      return render(request, 'home/list_books.html', {'livres': livres, 'auteurs': auteurs}) """




def list_books(request):
    if request.method == "POST":
        titre_livre = request.POST.get('titre_livre')
        code_auteur = request.POST.get('auteur')
        nbre_page = request.POST.get('nbre_page')
        prix = request.POST.get('prix')
        disponibilite = request.POST.get('disponibilite')
        image = request.FILES.get('image')
        auteur = Auteur.objects.get(code_auteur=code_auteur)
        Livre.objects.create(
            titre_livre=titre_livre,
            auteur=auteur,
            nbre_page=nbre_page,
            prix=prix,
            image=image,
        )
        return redirect('list_books')

    # Capture de la recherche
    query = request.GET.get('search') 
    if query:
        livres = Livre.objects.filter(titre_livre__icontains=query)  
    else:
        livres = Livre.objects.all()

    auteurs = Auteur.objects.all()
    return render(request, 'home/list_books.html', {'livres': livres, 'auteurs': auteurs, 'query': query})




#afficher les auteurs
def authors_view(request):
    if request.method == "POST":
        nom_auteur = request.POST.get('nom_auteur')
        prenom_auteur = request.POST.get('prenom_auteur')
        image = request.FILES.get('image')  # Récupérer l'image seulement si elle est envoyée

        # Créer l'auteur avec l'image
        Auteur.objects.create(
            nom_auteur=nom_auteur,
            prenom_auteur=prenom_auteur,
            image=image
        )
        return redirect('authors_view')

    auteurs = Auteur.objects.all()
    return render(request, 'home/authors.html', {'auteurs': auteurs})




#detail livre
def book_detail(request, code_livre):
    livre = get_object_or_404(Livre, code_livre=code_livre)
    auteurs = Auteur.objects.all()
    return render(request, 'home/book_detail.html', {'livre': livre,  'auteurs': auteurs})

#update livre 
def book_update(request, code_livre):
    livre = get_object_or_404(Livre, code_livre=code_livre)
    if request.method == 'POST':
        titre = request.POST.get('titre_livre')
        auteur_id = request.POST.get('auteur')
        prix = request.POST.get('prix')
        disponibilite = request.POST.get('disponibilite') == "True"
        livre.titre_livre = titre
        livre.auteur_id = auteur_id
        livre.prix = prix
        livre.disponibilite = disponibilite

        if 'image' in request.FILES:
            livre.image = request.FILES['image']

        livre.save()
        messages.success(request, 'Livre mis à jour avec succès !')
        return redirect('book_detail', code_livre=code_livre)
    return render(request, 'book_update.html', {'livre': livre})


#suppression livre 
def book_delete(request, code_livre):
    livre = get_object_or_404(Livre, code_livre=code_livre)
    
    livre.delete()
    
    messages.success(request, "Le livre a été supprimé avec succès.")
    
    return redirect('list_books')

#Modifier un auteur 
def edit_author(request):
    if request.method == 'POST':
        author_id = request.POST.get('code_auteur')
        nom_auteur = request.POST.get('nom_auteur')
        prenom_auteur = request.POST.get('prenom_auteur')
        image = request.FILES.get('image')

        try:
            auteur = get_object_or_404(Auteur, code_auteur=author_id)
            auteur.nom_auteur = nom_auteur
            auteur.prenom_auteur = prenom_auteur

            if image:
                auteur.image = image

            auteur.save()
            messages.success(request, "Author updated successfully!")
            return redirect('authors_view')
        except Auteur.DoesNotExist:
            messages.error(request, "Author not found.")
            return redirect('authors_view')
    return JsonResponse({'error': 'Invalid request'}, status=400)

#creer emprunts
def emprunt(request):
    return render(request, 'home/emprunt.html')


#creation d'un emprunt
def creer_emprunt(request):
    if request.method == "POST":
        adherent_id = request.POST.get("adherent_id")
        livre_id = request.POST.get("livre_id")

        # Récupérer l'adhérent et le livre
        try:
            adherent = Adherent.objects.get(code_adh=adherent_id)
            livre = Livre.objects.get(code_livre=livre_id)
        except (Adherent.DoesNotExist, Livre.DoesNotExist):
            messages.error(request, "Adhérent ou livre introuvable.")
            return redirect("creer_emprunt")

        # Vérifier si le livre est disponible
        if livre.exemplaires_disponibles <= 0:
            messages.error(request, "Ce livre n'est plus disponible.")
            return redirect("creer_emprunt")
         # Vérifier si l'adhérent a déjà emprunté ce livre
        deja_emprunte = Emprunt.objects.filter(adherent=adherent, livre=livre, date_retour__gte=date.today()).exists()
        if deja_emprunte:
            return JsonResponse({'erreur': 'Vous avez déjà emprunté ce livre.'}, status=400)

        # Créer l'emprunt
        emprunt = Emprunt.objects.create(
            adherent=adherent,
            livre=livre,
            date_retour=(datetime.now() + timedelta(days=15)).date()
        )

        # Réduire le nombre d'exemplaires disponibles
        livre.exemplaires_disponibles -= 1
        livre.save()

        messages.success(request, f"Emprunt de '{livre.titre_livre}' créé avec succès.")
        return redirect("emprunt")

    # Liste des adhérents et livres disponibles
    adherents = Adherent.objects.all()
    livres = Livre.objects.filter(exemplaires_disponibles__gt=0)
    return render(request, "home/creer_emprunt.html", {"adherents": adherents, "livres": livres})
# afficher emprunts
def emprunt(request):
    emprunts = Emprunt.objects.select_related('adherent', 'livre').all()
     # Grouper les emprunts par livre
    #grouped_emprunts = {}
    grouped_emprunts = {}
    emprunts = Emprunt.objects.all()
    for emprunt in emprunts:
        if emprunt.livre not in grouped_emprunts:
            grouped_emprunts[emprunt.livre] = []
        grouped_emprunts[emprunt.livre].append(emprunt)

    return render(request, "home/emprunt.html", {"grouped_emprunts": grouped_emprunts})
# detail emprunt
def detail_emprunt(request, emprunt_id):
    emprunt = get_object_or_404(Emprunt, id=emprunt_id)
    return render(request, 'home/detail_emprunt.html', {'emprunt': emprunt})

#Retourner livre
def retour_livre(request, emprunt_id):
    # Récupérer l'emprunt
    emprunt = get_object_or_404(Emprunt, id=emprunt_id)

    # Vérifier si le livre a déjà été retourné
    if emprunt.date_retour_effective:
        messages.warning(request, "Ce livre a déjà été retourné.")
        return redirect('emprunt')

    # Marquer le livre comme retourné
    emprunt.date_retour_effective = now()
    emprunt.save()

    # Augmenter le nombre d'exemplaires disponibles pour le livre
    livre = emprunt.livre
    livre.exemplaires_disponibles += 1
    livre.save()

    # Réduire le nombre d'emprunts actifs de l'adhérent
    adherent = emprunt.adherent
    adherent.nbr_emprunts_adh -= 1
    adherent.save()

    messages.success(request, f"Le livre '{livre.titre_livre}' a été retourné avec succès.")
    return redirect('emprunt')


#supprimer emprunt
def supprimer_emprunt(request, emprunt_id):
    if request.method == "POST":
        emprunt = get_object_or_404(Emprunt, id=emprunt_id)
        emprunt.delete()
        messages.success(request, "L'emprunt a été supprimé avec succès.")
        return redirect('emprunt')  # Remplacez 'liste_emprunts' par le nom de votre URL pour la liste des emprunts
    messages.error(request, "Action non autorisée.")
    return redirect('emprunt')