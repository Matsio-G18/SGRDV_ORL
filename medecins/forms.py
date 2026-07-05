from django import forms
from django.contrib.auth.models import User
from .models import Medecin


class MedecinForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all().order_by('username'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Medecin
        fields = ['user', 'nom', 'prenom', 'specialite', 'telephone', 'numero_cabinet', 'disponibilite']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du médecin'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom du médecin'}),
            'specialite': forms.Select(attrs={'class': 'form-select'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'numero_cabinet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'N° cabinet'}),
            'disponibilite': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
