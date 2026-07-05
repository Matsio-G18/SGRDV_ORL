from django import forms
from .models import Paiement


class PaiementMobileMoneyForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = ['montant', 'description', 'mobile_money_number']
        widgets = {
            'montant': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Montant en €',
                'step': '0.01',
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Description du paiement (ex : consultation ORL)',
            }),
            'mobile_money_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numéro Mobile Money',
            }),
        }

    def clean_mobile_money_number(self):
        number = self.cleaned_data.get('mobile_money_number')
        if number and not number.isdigit():
            raise forms.ValidationError('Veuillez entrer un numéro valide contenant uniquement des chiffres.')
        return number
