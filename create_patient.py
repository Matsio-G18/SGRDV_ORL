import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SGRDV_ORL.settings')
django.setup()

from django.contrib.auth.models import User
from patients.models import Patient
from datetime import date

# Récupérer l'utilisateur testuser
user = User.objects.get(username='testuser')

# Créer un Patient associé
patient, created = Patient.objects.get_or_create(
    user=user,
    defaults={
        'nom': 'Testeur',
        'prenom': 'Django',
        'sexe': 'M',
        'date_naissance': date(1990, 1, 1),
        'telephone': '0123456789',
        'adresse': '123 Rue de Test, Paris',
        'groupe_sanguin': 'O+',
    }
)

if created:
    print(f"Patient créé : {patient}")
else:
    print(f"Patient déjà existant : {patient}")
