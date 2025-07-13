from django.conf import settings
from twilio.rest import Client
import logging

logger = logging.getLogger(__name__)

def send_whatsapp_alert(to_number, message):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=message,
            from_=settings.TWILIO_WHATSAPP_NUMBER,
            to=f'whatsapp:{to_number}'
        )
        logger.info(f"WhatsApp alert sent to {to_number}")
    except Exception as e:
        logger.error(f"Error sending WhatsApp alert to {to_number}: {e}")