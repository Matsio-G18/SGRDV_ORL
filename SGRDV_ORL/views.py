from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
#from twilio.rest import Client  # Pensez à faire : pip install twilio

def home(request):
    if request.method == "POST":
        # 1. Récupération des données du formulaire HTML
        name = request.POST.get('patient_name')
        phone = request.POST.get('patient_phone')
        email = request.POST.get('patient_email')
        service = request.POST.get('service')
        date = request.POST.get('appointment_date')

        # Mappage des motifs pour un affichage propre dans les messages
        services_dict = {
            'consultation_generale': 'Consultation ORL Générale',
            'audiometrie': 'Bilan Auditif / Audiométrie',
            'sinusite': 'Troubles des Sinus / Nez bouché',
            'pharyngite': 'Maux de Gorge / Cordes Vocales',
            'vertiges': 'Gestion des Vertiges / Équilibre'
        }
        service_nom = services_dict.get(service, service)

        # 2. ENVOI DE L'EMAIL AU PATIENT
        try:
            subject = "Confirmation de votre demande - Clinique BERNADETTE"
            message_content = (
                f"Bonjour {name},\n\n"
                f"Votre demande de consultation pour le motif '{service_nom}' le {date} "
                f"a bien été transmise à notre secrétariat médical.\n\n"
                f"Cordialement,\nL'équipe BERNADETTE ORL"
            )
            send_mail(
                subject,
                message_content,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Erreur d'envoi Email: {e}")

        # 3. ENVOI DU SMS VIA TWILIO (Votre numéro virtuel)
        # try:
        #     # Remplacez par vos vrais identifiants Twilio
        #     account_sid = 'VOTRE_TWILIO_ACCOUNT_SID'
        #     auth_token = 'VOTRE_TWILIO_AUTH_TOKEN'
        #     twilio_number = 'VOTRE_NUMERO_TWILIO' 

        #     client = Client(account_sid, auth_token)
        #     sms_body = f"Clinique BERNADETTE : Bonjour {name}, votre demande de RDV pour le {date} est validée. Un agent va vous contacter."

        #     client.messages.create(
        #         from_=twilio_number,
        #         to=phone,
        #         body=sms_body
        #     )
        # except Exception as e:
        #     print(f"Erreur d'envoi SMS: {e}")

        # 4. Message flash de succès et redirection pour vider le formulaire
        messages.success(request, "Votre demande a été envoyée avec succès !  un email de confirmation vous a été envoyés.")
        return redirect('home')  # Assurez-vous que le nom de votre route dans urls.py est bien 'home'

    # Si la requête est un GET, on affiche simplement la page
    return render(request, 'home.html')
