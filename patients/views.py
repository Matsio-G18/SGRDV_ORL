from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Patient
from .forms import PatientForm

@login_required
def index(request):
    return redirect('patients:list')

@login_required
def list_patients(request):
    if not request.user.is_superuser and not hasattr(request.user, 'medecin'):
        return redirect('comptes:index')

    search_query = request.GET.get('search', '')
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
        'search_query': search_query,
    }
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
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Le patient a été enregistré avec succès.")
            return redirect('patients:list')
        messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = PatientForm()

    return render(request, 'patients/creer_patient.html', {'form': form})

@login_required
def edit(request, id):
    if not request.user.is_superuser and not hasattr(request.user, 'medecin'):
        return redirect('comptes:index')

    patient = get_object_or_404(Patient, id=id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, "Les informations du patient ont été mises à jour.")
            return redirect('patients:detail', id=patient.id)
        messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = PatientForm(instance=patient)

    return render(request, 'patients/modifier_patient.html', {'form': form, 'patient': patient})

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
