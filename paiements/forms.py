from django import forms
from .models import Paiement


class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = ['patient', 'montant', 'mode_paiement', 'statut', 'description']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'montant': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Montant en FCFA',
                'step': '0.01',
            }),
            'mode_paiement': forms.Select(attrs={'class': 'form-select'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Description du paiement (ex : consultation ORL)',
            }),
        }
