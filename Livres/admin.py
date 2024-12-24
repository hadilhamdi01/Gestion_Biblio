from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import CustomUser, Adherent, Livre, Emprunt, Auteur


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    pass

@admin.register(Adherent)
class AdherentAdmin(admin.ModelAdmin):
    list_display = ('code_adh', 'nom_adh', 'nbr_emprunts_adh')
    search_fields = ('nom_adh',)
    list_filter = ('nbr_emprunts_adh',)

@admin.register(Livre)
class LivreAdmin(admin.ModelAdmin):
    list_display = ('code_livre', 'titre_livre', 'auteur', 'disponibilite')
    search_fields = ('titre_livre',)
    list_filter = ('disponibilite', 'auteur')

@admin.register(Emprunt)
class EmpruntAdmin(admin.ModelAdmin):
    list_display = ('adherent', 'livre', 'date_emprunt', 'date_retour')
    search_fields = ('adherent__nom_adh', 'livre__titre_livre')
    list_filter = ('date_emprunt', 'date_retour')

@admin.register(Auteur)
class AuteurAdmin(admin.ModelAdmin):
    list_display = ('code_auteur', 'nom_auteur', 'prenom_auteur')
    search_fields = ('nom_auteur', 'prenom_auteur')