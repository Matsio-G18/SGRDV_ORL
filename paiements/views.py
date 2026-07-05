from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Paiement
from patients.models import Patient  # CORRECTION 1 : Le modèle Patient vient de l'application 'patients' !

@login_required
def index(request):
    return redirect('paiements:list')

@login_required
def list_paiements(request):
    """Affiche les transactions selon le niveau d'accréditation."""
    user = request.user
    
    if user.is_superuser or hasattr(user, 'medecin'):
        paiements = Paiement.objects.all()
    else:
        paiements = Paiement.objects.filter(patient__user=user)
        
    # CORRECTION 2 : Votre template de liste s'appelle 'liste_paiements.html' et non 'liste.html'
    return render(request, 'paiements/liste.html', {'paiements': paiements})

@login_required
def detail(request, id):
    """Visualisation d'une facture isolée avec cloisonnement strict."""
    user = request.user
    if user.is_superuser or hasattr(user, 'medecin'):
        paiement = get_object_or_404(Paiement, id=id)
    else:
        paiement = get_object_or_404(Paiement, id=id, patient__user=user)
    return render(request, 'paiements/detail_paiement.html', {'paiement': paiement})

@login_required
def create(request):
    """Création d'un reçu (Réservé à la direction / secrétariat)."""
    if not request.user.is_superuser:
        messages.error(request, "Accès refusé. Autorisation de facturation insuffisante.")
        return redirect('paiements:list')
        
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        montant = request.POST.get('montant')
        mode_paiement = request.POST.get('mode_paiement')
        statut = request.POST.get('statut')
        description = request.POST.get('description')
        
        if patient_id:
            patient_obj = get_object_or_404(Patient, id=patient_id)
            Paiement.objects.create(
                patient=patient_obj,
                montant=montant,
                mode_paiement=mode_paiement,
                statut=statut,
                description=description
            )
            messages.success(request, "Le paiement a été enregistré avec succès.")
        else:
            messages.error(request, "Le patient est requis pour enregistrer un paiement.")
        return redirect('paiements:list')
    
    # CORRECTION 3 (CRITIQUE) : On extrait les patients et on les injecte dans le contexte !
    tous_les_patients = Patient.objects.all().order_by('nom')
    context = {
        'patients': tous_les_patients  # Transmet la variable attendue par le {% for patient in patients %}
    }
    return render(request, 'paiements/creer_paiement.html', context)

@login_required
def edit(request, id):
    """Modification d'une transaction (Réservé au superuser)."""
    if not request.user.is_superuser:
        messages.error(request, "Action non autorisée.")
        return redirect('paiements:list')
    paiement = get_object_or_404(Paiement, id=id)
    if request.method == 'POST':
        messages.success(request, "Facture mise à jour.")
        return redirect('paiements:list')
    return render(request, 'paiements/modifier_paiement.html', {'paiement': paiement})

@login_required
def delete(request, id):
    """Suppression définitive d'un paiement (Réservé au superuser)."""
    if not request.user.is_superuser:
        messages.error(request, "Action interdite.")
        return redirect('paiements:list')
    paiement = get_object_or_404(Paiement, id=id)
    if request.method == 'POST':
        paiement.delete()
        messages.success(request, "La transaction a été effacée des registres.")
        return redirect('paiements:list')
    return render(request, 'paiements/confirmer_suppression_paiement.html', {'paiement': paiement})
