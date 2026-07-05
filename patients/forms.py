from django import forms
from .models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['user', 'nom', 'prenom', 'sexe', 'date_naissance', 'telephone', 'adresse', 'groupe_sanguin']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du patient'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom du patient'}),
            'sexe': forms.Select(attrs={'class': 'form-select'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Adresse complète'}),
            'groupe_sanguin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Groupe sanguin'}),
        }
