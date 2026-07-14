import logging

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
#from twilio.rest import Client  # Pensez à faire : pip install twilio

logger = logging.getLogger(__name__)

def home(request):
    if request.method == "POST":
        try:
            # 1. Récupération des données du formulaire HTML
            name = request.POST.get('patient_name', '').strip()
            phone = request.POST.get('patient_phone', '').strip()
            email = request.POST.get('patient_email', '').strip()
            service = request.POST.get('service', '').strip()
            date = request.POST.get('appointment_date', '').strip()

            # Validation des champs requis avant traitement
            if not name or not phone or not email or not service or not date:
                messages.error(request, "Tous les champs du formulaire doivent être remplis.")
                return render(request, 'home.html')

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
                    f"Votre demande de consultation pour le motif '{service_nom}' à cette date le {date} "
                    f"a bien été transmise à notre service de communication médical.\n\n"
                    f"Vous allez recevoir la confirmation dans les plus brefs délais.\n\n"
                    f"Cordialement,\nL'équipe BERNADETTE ORL"
                )
                send_mail(
                    subject,
                    message_content,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=True,
                )
            except Exception as e:
                logger.exception("Erreur d'envoi email pour la demande de consultation")
                messages.warning(request, "Votre demande a bien été reçue, mais l'email de confirmation n'a pas pu être envoyé.")
                return render(request, 'home.html')

            # 3. ENVOI DU SMS VIA TWILIO (Votre numéro virtuel)
            # try:
            #     # Remplacez par vos vrais identifiants Twilio
            #     account_sid = 'VOTRE_TWILIO_ACCOUNT_SID'
            #     auth_token = 'VOTRE_TWILIO_AUTH_TOKEN'
            #     twilio_number = 'VOTRE_NUMERO_TWILIO'
            #
            #     client = Client(account_sid, auth_token)
            #     sms_body = f"Clinique BERNADETTE : Bonjour {name}, votre demande de RDV pour le {date} est validée. Un agent va vous contacter."
            #
            #     client.messages.create(
            #         from_=twilio_number,
            #         to=phone,
            #         body=sms_body
            #     )
            # except Exception as e:
            #     logger.exception("Erreur d'envoi SMS pour la demande de consultation")

            messages.success(request, "Votre demande a été envoyée avec succès ! Un email de confirmation vous a été envoyé.")
            return redirect('home')
        except Exception as exc:
            logger.exception("Erreur lors du traitement d'une demande de consultation")
            messages.error(request, "Une erreur est survenue lors de l'envoi de votre demande. Veuillez réessayer ou contacter le support.")
            return render(request, 'home.html')

    # Si la requête est un GET, on affiche simplement la page
    return render(request, 'home.html')
