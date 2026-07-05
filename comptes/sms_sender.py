import logging
# Si vous utilisez Twilio plus tard : pip install twilio
# from twilio.rest import Client 

logger = logging.getLogger(__name__)

# def enviar_sms_twilio(numero_destinataire, corps_message):
#     """Configuration Twilio réelle (à activer en production)."""
#     # account_sid = 'VOTRE_ACCOUNT_SID'
#     # auth_token = 'VOTRE_AUTH_TOKEN'
#     # client = Client(account_sid, auth_token)
#     # message = client.messages.create(
#     #     from_='BERNADETTE',
#     #     body=corps_message,
#     #     to=numero_destinataire  # Format international ex: +242068209738
#     # )
#     pass

def envoyer_sms_confirmation(telephone, message):
    """Détecte les numéros du Congo et simule/envoie le SMS."""
    
    # Formatage automatique pour l'indicatif du Congo (+242)
    if telephone.startswith('06') or telephone.startswith('05'):
        numero_international = f"+242{telephone}"
    elif not telephone.startswith('+'):
        numero_international = f"+242{telephone}"
    else:
        numero_international = telephone

    # 1. Affichage de simulation dans le terminal de Django
    print("\n" + "="*50)
    print("📱 EXPÉDITION SMS AUTOMATIQUE (CLINIQUE BERNADETTE)")
    print(f"➡️ Destinataire : {numero_international}")
    print(f"💬 Message : {message}")
    print("="*50 + "\n")
    
    # # 2. Lien vers l'API réelle
    # try:
    #     enviar_sms_twilio(numero_international, message)
    # except Exception as e:
    #     logger.error(f"Échec de l'envoi du SMS réel via l'opérateur: {e}")
