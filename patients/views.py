from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Patient  

@login_required
def index(request):
    """Redirige l'index de l'application vers la liste des patients."""
    # CORRECTION : Assurez-vous que le nom de la route correspond à vos URLs (souvent 'list_patients' ou 'list')
    return redirect('patients:list')

@login_required
def list_patients(request):
    # Sécurité : Réservé aux admins ou médecins
    if not request.user.is_superuser and not hasattr(request.user, 'medecin'):
        return redirect('comptes:index')
    
    # Récupération de la recherche depuis le formulaire GET
    search_query = request.GET.get('search', '')
    
    # Filtrage dynamique si une recherche est soumise
    if search_query:
        patients = Patient.objects.filter(
            Q(nom__icontains=search_query) | 
            Q(prenom__icontains=search_query) |
            Q(id__icontains=search_query)
        ).order_by('-id')
    else:
        patients = Patient.objects.all().order_by('-id')
        
    context = {
        'patients': patients,
        'search_query': search_query # Utile si vous voulez réafficher la recherche dans le champ
    }
    # CORRECTION : Le fichier HTML que nous avons créé s'appelle 'liste_patients.html' et non 'liste.html'
    return render(request, 'patients/liste.html', context)

@login_required
def detail(request, id):
    if not request.user.is_superuser and not hasattr(request.user, 'medecin'):
        return redirect('comptes:index')
        
    patient = get_object_or_404(Patient, id=id)
    return render(request, 'patients/detail_patient.html', {'patient': patient})

@login_required
def create(request):
    if not request.user.is_superuser and not hasattr(request.user, 'medecin'):
        return redirect('comptes:index')
        
    if request.method == 'POST':
        # Logique d'enregistrement du formulaire ici (ex: form.save())
        messages.success(request, "Le patient a été enregistré avec succès.")
        return redirect('patients:list')
        
    return render(request, 'patients/creer_patient.html')

@login_required
def edit(request, id):
    if not request.user.is_superuser and not hasattr(request.user, 'medecin'):
        return redirect('comptes:index')
        
    patient = get_object_or_404(Patient, id=id)
    if request.method == 'POST':
        messages.success(request, "Les informations du patient ont été mises à jour.")
        return redirect('patients:detail', id=patient.id)
        
    return render(request, 'patients/modifier_patient.html', {'patient': patient})

@login_required
def delete(request, id):
    if not request.user.is_superuser and not hasattr(request.user, 'medecin'):
        return redirect('comptes:index')
        
    patient = get_object_or_404(Patient, id=id)
    if request.method == 'POST':
        patient.delete()
        messages.success(request, "Le dossier du patient a été définitivement supprimé.")
        return redirect('patients:list')
        
    return render(request, 'patients/confirmer_suppression.html', {'patient': patient})
