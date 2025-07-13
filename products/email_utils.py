"""
Email notification utilities for Deal Radar
Handles all email functionality without affecting the frontend
"""

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone
from .models import UserProfile, PriceAlert, TrackedProduct
from products.whatsapp_utils import send_whatsapp_alert
import logging

logger = logging.getLogger(__name__)

def send_price_alert_email(alert, old_price, new_price):
    """Send email notification for triggered price alerts"""
    user = alert.user
    product = alert.tracked_product.product

    try:
        profile = user.userprofile
    except Exception:
        profile = None

    # WhatsApp alert
    if profile and getattr(profile, 'whatsapp_notifications', False) and profile.whatsapp_number:
        message = (
            f"Deal Radar Alert: '{product.name}' has dropped from £{old_price} to £{new_price}!\n"
            f"Check it here: {product.url}"
        )
        send_whatsapp_alert(profile.whatsapp_number, message)

    # Email alert (existing logic)
    if profile and getattr(profile, 'email_notifications', True):
        subject = f"Price Drop Alert: {product.name}"
        context = {
            'user': user,
            'product': product,
            'old_price': old_price,
            'new_price': new_price,
            'site_name': 'Deal Radar',
        }
        html_message = render_to_string('emails/price_alert.html', context)
        plain_message = strip_tags(html_message)
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            return True
        except Exception as e:
            logger.error(f"Error sending price alert email: {e}")
            return False
    return True

def send_welcome_email(user):
    """Send welcome email to new users"""
    subject = '🎯 Welcome to Deal Radar!'
    
    context = {
        'user': user,
        'site_name': 'Deal Radar',
    }
    
    html_message = render_to_string('emails/welcome.html', context)
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Welcome email sent to {user.email}")
        return True
    except Exception as e:
        logger.error(f"Error sending welcome email: {e}")
        return False

def send_daily_summary_email(user):
    """Send daily summary of alerts and tracked products"""
    try:
        profile = user.userprofile
        if not profile.email_notifications or profile.notification_frequency != 'daily':
            logger.info(f"Daily summary not sent to {user.email}: notifications off or not daily.")
            return False
    except UserProfile.DoesNotExist:
        return False
    
    # Get today's triggered alerts
    today = timezone.now().date()
    triggered_today = PriceAlert.objects.filter(
        tracked_product__user=user,
        is_triggered=True,
        triggered_at__date=today
    ).select_related('tracked_product__product')
    
    # Get active tracked products
    tracked_products = TrackedProduct.objects.filter(
        user=user,
        is_active=True
    ).select_related('product')
    
    if not triggered_today.exists() and not tracked_products.exists():
        return False
    
    subject = f'📊 Daily Deal Radar Summary - {today.strftime("%B %d, %Y")}'
    
    context = {
        'user': user,
        'triggered_alerts': triggered_today,
        'tracked_products': tracked_products,
        'date': today,
        'site_name': 'Deal Radar',
        'site_url': settings.SITE_DOMAIN,
    }
    
    html_message = render_to_string('emails/daily_summary.html', context)
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Daily summary email sent to {user.email}")
        return True
    except Exception as e:
        logger.error(f"Error sending daily summary: {e}")
        return False