from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Notification, RendezVous
from .forms import RendezVousForm
from patients.models import Patient # Utile pour la création de rendez-vous
from medecins.models import Medecin

@login_required
def index(request):
    """Redirige l'index vers la liste sécurisée des rendez-vous."""
    return redirect('rdv:list')

@login_required
def list_rdv(request):
    """Affiche les rendez-vous selon le rôle de l'utilisateur."""
    user = request.user
    
    if user.is_superuser or hasattr(user, 'medecin'):
        # Les médecins et administrateurs visualisent tout l'agenda ORL
        rendezvous = RendezVous.objects.all().order_by('date_rdv', 'heure_rdv')
    else:
        # Le patient connecté ne voit strictement que ses propres rendez-vous
        rendezvous = RendezVous.objects.filter(patient__user=user).order_by('date_rdv', 'heure_rdv')
        
    return render(request, 'rdv/liste.html', {'rendezvous': rendezvous})

@login_required
def detail(request, id):
    """Affiche les détails d'un rendez-vous spécifique avec contrôle d'accès."""
    user = request.user
    
    if user.is_superuser or hasattr(user, 'medecin'):
        rdv = get_object_or_404(RendezVous, id=id)
    else:
        # Sécurité : Le patient ne peut charger le rendez-vous que s'il lui appartient
        rdv = get_object_or_404(RendezVous, id=id, patient__user=user)
        
    return render(request, 'rdv/detail_rdv.html', {'rdv': rdv})

@login_required
def create(request):
    """Gère la création d'un nouveau rendez-vous."""
    if request.method == 'POST':
        form = RendezVousForm(request.POST, user=request.user)
        if form.is_valid():
            rdv = form.save(commit=False)
            # Associer le patient connecté si disponible
            if hasattr(request.user, 'patient') and request.user.patient is not None:
                rdv.patient = request.user.patient
            else:
                # Si l'utilisateur n'est pas patient, laisser None (ou gérer différemment)
                rdv.patient = None
            rdv.save()

            # Notifications envoyées aux administrateurs et au médecin concerné
            notification_message = (
                f"Nouvelle demande de rendez-vous de {rdv.patient} "
                f"le {rdv.date_rdv} à {rdv.heure_rdv} ({rdv.get_motif_display})."
            )
            notification_url = reverse('rdv:detail', args=[rdv.id])
            recipients = list(User.objects.filter(is_superuser=True))

            if rdv.medecin and rdv.medecin.user:
                if rdv.medecin.user not in recipients:
                    recipients.append(rdv.medecin.user)

            for recipient in recipients:
                Notification.objects.create(
                    recipient=recipient,
                    rdv=rdv,
                    message=notification_message,
                    url=notification_url,
                )

            messages.success(request, "Votre demande de rendez-vous a été enregistrée et est en attente.")
            return redirect('rdv:list')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = RendezVousForm(user=request.user)
        
    return render(request, 'rdv/creer_rdv.html', {'form': form})

@login_required
def notifications(request):
    notif_list = request.user.notifications.order_by('-created_at')

    if request.method == 'POST':
        notif_list.filter(is_read=False).update(is_read=True)
        messages.success(request, "Toutes les notifications ont été marquées comme lues.")
        return redirect('rdv:notifications')

    return render(request, 'rdv/notifications.html', {'notifications': notif_list})


@login_required
def edit(request, id):
    """Permet de modifier un rendez-vous (restreint ou complet selon le rôle)."""
    user = request.user
    
    if user.is_superuser or hasattr(user, 'medecin'):
        rdv = get_object_or_404(RendezVous, id=id)
    else:
        # Sécurité : Un patient ne peut modifier que sa propre demande
        rdv = get_object_or_404(RendezVous, id=id, patient__user=user)
        
    if request.method == 'POST':
        form = RendezVousForm(request.POST, instance=rdv, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Le rendez-vous a été modifié avec succès.")
            return redirect('rdv:list')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
    else:
        form = RendezVousForm(instance=rdv, user=request.user)

    return render(request, 'rdv/modifier_rdv.html', {'form': form, 'rdv': rdv})

@login_required
def delete(request, id):
    """Supprime ou annule un rendez-vous de manière sécurisée."""
    user = request.user
    
    if user.is_superuser or hasattr(user, 'medecin'):
        rdv = get_object_or_404(RendezVous, id=id)
    else:
        # Sécurité : Un patient ne peut supprimer/annuler que son propre rendez-vous
        rdv = get_object_or_404(RendezVous, id=id, patient__user=user)
        
    if request.method == 'POST':
        rdv.delete()
        messages.success(request, "Le rendez-vous a été annulé avec succès.")
        return redirect('rdv:list')
        
    return render(request, 'rdv/confirmer_suppression_rdv.html', {'rdv': rdv})
