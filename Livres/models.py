from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Ajoutez des champs personnalisés si nécessaire
    contact = models.CharField(max_length=15, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
