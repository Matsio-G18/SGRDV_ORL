from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Paiement
from .forms import PaiementForm

@login_required
def index(request):
    return redirect('paiements:list')

@login_required
def list_paiements(request):
    user = request.user
    if user.is_superuser or hasattr(user, 'medecin'):
        paiements = Paiement.objects.all()
    else:
        paiements = Paiement.objects.filter(patient__user=user)
    return render(request, 'paiements/liste.html', {'paiements': paiements})

@login_required
def detail(request, id):
    user = request.user
    if user.is_superuser or hasattr(user, 'medecin'):
        paiement = get_object_or_404(Paiement, id=id)
    else:
        paiement = get_object_or_404(Paiement, id=id, patient__user=user)
    return render(request, 'paiements/detail_paiement.html', {'paiement': paiement})

@login_required
def create(request):
    if not request.user.is_superuser:
        messages.error(request, "Accès refusé. Autorisation de facturation insuffisante.")
        return redirect('paiements:list')

    if request.method == 'POST':
        form = PaiementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Le paiement a été enregistré avec succès.")
            return redirect('paiements:list')
        messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = PaiementForm()

    return render(request, 'paiements/creer_paiement.html', {'form': form})

@login_required
def edit(request, id):
    if not request.user.is_superuser:
        messages.error(request, "Action non autorisée.")
        return redirect('paiements:list')

    paiement = get_object_or_404(Paiement, id=id)
    if request.method == 'POST':
        form = PaiementForm(request.POST, instance=paiement)
        if form.is_valid():
            form.save()
            messages.success(request, "Facture mise à jour.")
            return redirect('paiements:list')
        messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = PaiementForm(instance=paiement)

    return render(request, 'paiements/modifier_paiement.html', {'form': form, 'paiement': paiement})

@login_required
def delete(request, id):
    if not request.user.is_superuser:
        messages.error(request, "Action interdite.")
        return redirect('paiements:list')
    paiement = get_object_or_404(Paiement, id=id)
    if request.method == 'POST':
        paiement.delete()
        messages.success(request, "La transaction a été effacée des registres.")
        return redirect('paiements:list')
    return render(request, 'paiements/confirmer_suppression_paiement.html', {'paiement': paiement})
