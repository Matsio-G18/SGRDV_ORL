from django import forms
from .models import RendezVous
from medecins.models import Medecin

class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = ['medecin', 'date_rdv', 'heure_rdv', 'motif', 'notes']
        widgets = {
            'date_rdv': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'heure_rdv': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'motif': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'medecin': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Si vous voulez filtrer la liste des médecins selon un critère, faites-le ici
        self.fields['medecin'].queryset = Medecin.objects.all()
        self.fields['medecin'].required = False
