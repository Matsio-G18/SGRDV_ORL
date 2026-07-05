from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Medecin
from .forms import MedecinForm

@login_required
def index(request):
    return redirect('medecins:list')

@login_required
def list_medecins(request):
    search_query = request.GET.get('search', '')

    if search_query:
        medecins = Medecin.objects.filter(
            Q(nom__icontains=search_query) |
            Q(prenom__icontains=search_query) |
            Q(specialite__icontains=search_query)
        ).order_by('nom')
    else:
        medecins = Medecin.objects.all().order_by('nom')

    context = {
        'medecins': medecins,
        'search_query': search_query,
    }
    return render(request, 'medecins/liste.html', context)

@login_required
def detail(request, id):
    medecin = get_object_or_404(Medecin, id=id)
    return render(request, 'medecins/detail_medecin.html', {'medecin': medecin})

@login_required
def create(request):
    if not request.user.is_superuser:
        messages.error(request, "Accès refusé. Réservé à la direction de la clinique.")
        return redirect('medecins:list')

    if request.method == 'POST':
        form = MedecinForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Le profil du médecin a été créé avec succès.")
            return redirect('medecins:list')
        messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = MedecinForm()

    users = User.objects.all().order_by('username')
    return render(request, 'medecins/creer_medecin.html', {'form': form, 'users': users})

@login_required
def edit(request, id):
    medecin = get_object_or_404(Medecin, id=id)
    if not request.user.is_superuser and request.user != medecin.user:
        messages.error(request, "Vous ne pouvez pas modifier le profil d'un confrère.")
        return redirect('medecins:list')

    if request.method == 'POST':
        form = MedecinForm(request.POST, instance=medecin)
        if form.is_valid():
            form.save()
            messages.success(request, "Les modifications ont été enregistrées.")
            return redirect('medecins:list')
        messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = MedecinForm(instance=medecin)

    return render(request, 'medecins/modifier_medecin.html', {'form': form, 'medecin': medecin})

@login_required
def delete(request, id):
    if not request.user.is_superuser:
        messages.error(request, "Action interdite.")
        return redirect('medecins:list')

    medecin = get_object_or_404(Medecin, id=id)
    if request.method == 'POST':
        medecin.delete()
        messages.success(request, "Le profil a été retiré du système.")
        return redirect('medecins:list')

    return render(request, 'medecins/confirmer_suppression_medecin.html', {'medecin': medecin})
