from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta, date
from django.core.exceptions import ValidationError



# Model de user pour l'authentification
class CustomUser(AbstractUser):
    contact = models.CharField(max_length=15, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


# Model d'adhérent
class Adherent(models.Model):
    code_adh = models.AutoField(primary_key=True)
    nom_adh = models.CharField(max_length=100)
    nbr_emprunts_adh = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='adherents/', null=True, blank=True )

    def __str__(self):
        return self.nom_adh


# Model de livre
class Livre(models.Model):
    code_livre = models.AutoField(primary_key=True)
    titre_livre = models.CharField(max_length=200)
    nbre_page = models.PositiveIntegerField()
    auteur = models.ForeignKey('Auteur', on_delete=models.CASCADE, related_name='livres')
    image = models.ImageField(upload_to='livres/', null=True, blank=True)  
    prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    disponibilite = models.BooleanField(default=True)  
    total_exemplaires = models.PositiveIntegerField(default=3)  
    exemplaires_disponibles = models.PositiveIntegerField(default=3)

    def __str__(self):
        return self.titre_livre


# Model d'emprunt
class Emprunt(models.Model):
    adherent = models.ForeignKey(Adherent, on_delete=models.CASCADE, related_name='emprunts')
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='emprunts')
    date_emprunt = models.DateField(auto_now_add=True)
    date_retour = models.DateField()

    def clean(self):
        if Emprunt.objects.filter(adherent=self.adherent, livre=self.livre, date_retour__gte=date.today()).exists():
            raise ValidationError("Vous avez déjà emprunté ce livre.")

    def save(self, *args, **kwargs):
        if not self.date_retour:
            self.date_retour = self.date_emprunt + timedelta(days=15)
        super().save(*args, **kwargs)
        # Mettre à jour le nombre d'emprunts de l'adhérent
        self.adherent.nbr_emprunts_adh += 1
        self.adherent.save()


    def __str__(self):
        return f"Emprunt: {self.adherent} -> {self.livre}"


# Model d'auteur
class Auteur(models.Model):
    code_auteur = models.AutoField(primary_key=True)
    nom_auteur = models.CharField(max_length=100)
    prenom_auteur = models.CharField(max_length=100)
    image = models.ImageField(upload_to='auteurs/', null=True, blank=True)

    def __str__(self):
        return f"{self.nom_auteur} {self.prenom_auteur}"



