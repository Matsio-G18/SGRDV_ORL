from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Medecin

@login_required
def index(request):
    
    return redirect('medecins:list')

@login_required
def list_medecins(request):
    """Affiche l'annuaire des médecins de la clinique BERNADETTE."""
    # Récupération de la recherche depuis le formulaire GET
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
        'search_query': search_query
    }
    # CORRECTION : On cible le fichier liste_medecins.html
    return render(request, 'medecins/liste.html', context)

@login_required
def detail(request, id):
    """Affiche la fiche détaillée d'un médecin ORL."""
    medecin = get_object_or_404(Medecin, id=id)
    return render(request, 'medecins/detail_medecin.html', {'medecin': medecin})

@login_required
def create(request):
    """Permet d'ajouter un nouveau médecin (Sécurisé pour l'admin)."""
    if not request.user.is_superuser:
        messages.error(request, "Accès refusé. Réservé à la direction de la clinique.")
        return redirect('medecins:list')
        
    if request.method == 'POST':
        messages.success(request, "Le profil du médecin a été créé avec succès.")
        return redirect('medecins:list')
        
    return render(request, 'medecins/creer_medecin.html')

@login_required
def edit(request, id):
    """Permet de modifier les informations d'un praticien (Sécurisé)."""
    medecin = get_object_or_404(Medecin, id=id)
    
    # Un médecin ne modifie que son profil, le superuser peut tout modifier
    if not request.user.is_superuser and request.user != medecin.user:
        messages.error(request, "Vous ne pouvez pas modifier le profil d'un confrère.")
        return redirect('medecins:list')
        
    if request.method == 'POST':
        messages.success(request, "Les modifications ont été enregistrées.")
        return redirect('medecins:list')
        
    return render(request, 'medecins/modifier_medecin.html', {'medecin': medecin})

@login_required
def delete(request, id):
    """Supprime un médecin du répertoire (Strictement réservé au superuser)."""
    if not request.user.is_superuser:
        messages.error(request, "Action interdite.")
        return redirect('medecins:list')
        
    medecin = get_object_or_404(Medecin, id=id)
    if request.method == 'POST':
        medecin.delete()
        messages.success(request, "Le profil a été retiré du système.")
        return redirect('medecins:list')
        
    return render(request, 'medecins/confirmer_suppression_medecin.html', {'medecin': medecin})
