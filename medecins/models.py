from django.db import models
from django.contrib.auth.models import User

class Medecin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='medecin', null=True, blank=True)
    nom = models.CharField(max_length=100)
    specialite = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return self.nom
