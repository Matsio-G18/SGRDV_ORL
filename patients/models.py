from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    # Liste des choix pour le sexe
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    # Lien obligatoire avec le compte de connexion
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient', null=True, blank=True)
    
    # Vos champs d'origine
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    
    # Nouveau champ Sexe avec menu déroulant
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, default='M')
    
    date_naissance = models.DateField()
    telephone = models.CharField(max_length=20)
    
    # Ajouts recommandés
    adresse = models.TextField(blank=True, null=True)
    groupe_sanguin = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"
