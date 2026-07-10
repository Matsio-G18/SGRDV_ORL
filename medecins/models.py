from django.db import models
from django.contrib.auth.models import User

class Medecin(models.Model):
    SPECIALITE_CHOICES = [
        ('orl_generale', 'ORL Générale'),
        ('audiologie', "Audiologie / Troubles de l'audition"),
        ('rhinologie', 'Rhinologie / Sinus et cloisons nasales'),
        ('laryngologie', 'Laryngologie / Voix et cordes vocales'),
        ('orl_pediatrique', 'ORL Pédiatrique'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='medecin', null=True, blank=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100, blank=True, default='')
    specialite = models.CharField(max_length=50, choices=SPECIALITE_CHOICES, default='orl_generale')
    telephone = models.CharField(max_length=20)
    numero_cabinet = models.CharField(max_length=50, blank=True, default='')
    disponibilite = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}".strip()
