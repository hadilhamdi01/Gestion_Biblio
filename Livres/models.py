from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta


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

    def __str__(self):
        return self.nom_adh


# Model de livre
class Livre(models.Model):
    code_livre = models.AutoField(primary_key=True)
    titre_livre = models.CharField(max_length=200)
    nbre_page = models.PositiveIntegerField()
    auteur = models.ForeignKey('Auteur', on_delete=models.CASCADE, related_name='livres')
    image = models.ImageField(upload_to='livres/', null=True, blank=True)  # Ajout de l'image
    disponibilite = models.BooleanField(default=True)  # Indique si le livre est disponible

    def __str__(self):
        return self.titre_livre


# Model d'emprunt
class Emprunt(models.Model):
    adherent = models.ForeignKey(Adherent, on_delete=models.CASCADE, related_name='emprunts')
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE, related_name='emprunts')
    date_emprunt = models.DateField(auto_now_add=True)
    date_retour = models.DateField()

    def save(self, *args, **kwargs):
        # Calcul automatique de la date de retour à 15 jours après l'emprunt
        if not self.date_retour:
            self.date_retour = self.date_emprunt + timedelta(days=15)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Emprunt: {self.adherent} -> {self.livre}"


# Model d'auteur
class Auteur(models.Model):
    code_auteur = models.AutoField(primary_key=True)
    nom_auteur = models.CharField(max_length=100)
    prenom_auteur = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom_auteur} {self.prenom_auteur}"
