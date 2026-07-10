from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from patients.models import Patient
from rdv.models import RendezVous, Notification
import datetime
import uuid

from .sms_sender import envoyer_sms_confirmation

def index(request):
    """Page d'accueil publique : affiche le formulaire en premier lieu."""
    
    if request.method == 'POST':
        # Récupération des données du formulaire anonyme ou connecté
        nom_patient = request.POST.get('patient_name', '').strip()
        telephone = request.POST.get('patient_phone', '').strip()
        motif = request.POST.get('service')
        date_souhaitee = request.POST.get('appointment_date')
        
        # Nettoyage rapide du numéro (évite le crash si le numéro est vide)
        telephone_propre = telephone.replace(" ", "") if telephone else ""
        
        # Vérification des champs obligatoires du formulaire de contact
        if not nom_patient or not telephone or not date_souhaitee or not motif:
            messages.error(request, "Veuillez remplir tous les champs obligatoires du formulaire.")
            return redirect('comptes:index')

        # 1. Gestion du profil Patient
        if request.user.is_authenticated and hasattr(request.user, 'patient'):
            patient_obj = request.user.patient
        else:
            # Recherche ou création d'une fiche Patient basée sur le numéro de téléphone
            patient_obj, created = Patient.objects.get_or_create(
                telephone=telephone_propre,
                defaults={
                    'nom': nom_patient,
                    'prenom': '(Visiteur)',
                    'date_naissance': datetime.date.today(), # Date par défaut à modifier au guichet
                    'sexe': 'M'
                }
            )

        # 2. Enregistrement de la demande de Rendez-vous
        nouveau_rdv = RendezVous.objects.create(
            patient=patient_obj,
            date_rdv=date_souhaitee,
            heure_rdv="08:00:00", # Heure par défaut en attente de traitement par le secrétariat
            motif=motif,
            statut='EN_ATTENTE',
            notes=f"Demande soumise en libre accès par : {nom_patient}"
        )
        
        # Notification de succès à l'écran
        messages.success(
            request, 
            f"Merci {nom_patient}, votre demande de consultation pour le {date_souhaitee} "
            f"a été enregistrée avec succès sous la référence #RDV-{nouveau_rdv.id}."
        )
        
        # Envoi du SMS avec les bonnes variables d'instance
        if telephone_propre:
            message_texte = f"BERNADETTE ORL: Bonjour {nom_patient}, votre demande du {date_souhaitee} a bien ete recue (Ref: #RDV-{nouveau_rdv.id}). Notre secretariat va vous recontacter."
            envoyer_sms_confirmation(telephone_propre, message_texte)

        # --- Gestion de l'email : liaison utilisateur, notification et envoi d'email ---
        patient_email = request.POST.get('patient_email', '').strip()
        if patient_email:
            # Si un User existe déjà avec cet email, on le récupère
            user_obj = User.objects.filter(email__iexact=patient_email).first()

            # Si aucun user, on crée un compte minimal (mot de passe inutilisable)
            if not user_obj:
                # Générer un username unique à partir de l'email
                base_username = patient_email.split('@')[0]
                username = base_username
                if User.objects.filter(username=username).exists():
                    username = f"{base_username}_{uuid.uuid4().hex[:6]}"
                user_obj = User.objects.create_user(username=username, email=patient_email)
                user_obj.set_unusable_password()
                user_obj.save()

            # Associer le patient existant au user si non associé
            if not hasattr(patient_obj, 'user') or patient_obj.user is None:
                patient_obj.user = user_obj
                patient_obj.save()

            # Créer une notification pour l'utilisateur patient
            try:
                notif_message = f"Votre demande de RDV #{nouveau_rdv.id} pour le {date_souhaitee} a bien été reçue."
                notif_url = reverse('rdv:detail', args=[nouveau_rdv.id])
                Notification.objects.create(recipient=user_obj, rdv=nouveau_rdv, message=notif_message, url=notif_url)
            except Exception:
                # Ne pas planter l'envoi si le modèle Notification rencontre un problème
                pass

            # Envoi d'un email de confirmation (si la configuration email est présente)
            try:
                subject = "Confirmation de demande de rendez-vous - BERNADETTE"
                email_body = (
                    f"Bonjour {nom_patient},\n\nNous avons bien reçu votre demande de rendez-vous pour le {date_souhaitee}.\n"
                    f"Référence : RDV-{nouveau_rdv.id}\n\nNotre secrétariat vous contactera prochainement.\n\nCordialement,\nBERNADETTE ORL"
                )
                send_mail(subject, email_body, getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@sgrdv-orl.local'), [patient_email], fail_silently=True)
            except Exception:
                pass
            
        # Redirection vers l'accueil pour afficher le message de succès
        return redirect('/')

    # Si c'est une requête GET, on affiche simplement la page d'accueil avec son formulaire
    return render(request, 'home.html')


def login_view(request):
    """Gère la connexion des utilisateurs."""
    if request.user.is_authenticated:
        return redirect('comptes:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue, {username} !")
                return redirect('comptes:index')
        else:
            messages.error(request, "Identifiant ou mot de passe incorrect.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'comptes/login.html', {'form': form})

def logout_view(request):
    """Gère la déconnexion de l'utilisateur."""
    logout(request)
    messages.info(request, "Vous avez été déconnecté avec succès.")
    return redirect('comptes:index')

def register(request):
    """Gère l'inscription des nouveaux patients."""
    if request.user.is_authenticated:
        return redirect('comptes:index')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre compte a été créé ! Vous pouvez maintenant vous connecter.")
            return redirect('comptes:login')
        else:
            messages.error(request, "Erreur lors de l'inscription. Veuillez vérifier les informations.")
    else:
        form = UserCreationForm()
        
    return render(request, 'comptes/register.html', {'form': form})
