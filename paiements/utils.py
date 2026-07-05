import logging
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def send_payment_email(subject, message, recipient_list, html_message=None):
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@bernadette-orl.local')
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_message,
        fail_silently=False,
    )


def send_payment_sms(phone_number, text):
    backend = getattr(settings, 'SMS_BACKEND', 'console')
    if backend == 'console':
        logger.info('[SMS][console] %s -> %s', phone_number, text)
        return True

    # Implémentation future pour un provider réel.
    logger.warning('SMS backend inconnu: %s. Message non envoyé.', backend)
    return False
