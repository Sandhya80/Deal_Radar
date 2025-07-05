from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from products.models import PriceAlert
from django.utils import timezone
from decimal import Decimal

class Command(BaseCommand):
    help = 'Check for price drops and send email alerts'

    def handle(self, *args, **options):
        # Get all active price alerts
        active_alerts = PriceAlert.objects.filter(
            is_enabled=True,
            is_triggered=False
        ).select_related('tracked_product__product', 'tracked_product__user')
        
        triggered_count = 0
        
        for alert in active_alerts:
            product = alert.tracked_product.product
            current_price = product.current_price
            target_price = alert.target_price
            
            # Check if current price is at or below target price
            if current_price <= target_price:
                # Send email notification
                self.send_price_alert_email(alert)
                
                # Mark alert as triggered
                alert.is_triggered = True
                alert.triggered_at = timezone.now()
                alert.save()
                
                triggered_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Alert triggered for {product.name}: £{current_price} <= £{target_price}'
                    )
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Checked {active_alerts.count()} alerts, triggered {triggered_count}')
        )
    
    def send_price_alert_email(self, alert):
        """Send email notification for price alert"""
        product = alert.tracked_product.product
        user = alert.tracked_product.user
        
        # Skip if user has no email
        if not user.email:
            self.stdout.write(f'No email for user {user.username}')
            return
        
        subject = f'🚨 Price Alert: {product.name} - Deal Radar'
        message = f"""
Hi {user.first_name or user.username},

Great news! The price for "{product.name}" has dropped to your target price!

💰 Current Price: £{product.current_price}
🎯 Your Target: £{alert.target_price}
💵 You Save: £{alert.target_price - product.current_price if alert.target_price > product.current_price else 0}

📦 Product Details:
• Name: {product.name}
• Category: {product.category}
• Site: {product.site_name}
• Link: {product.url}

🛒 Don't miss this deal - prices can change quickly!

Best regards,
Deal Radar Team

---
To manage your price alerts, visit: http://127.0.0.1:8000/dashboard/
        """
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            self.stdout.write(f'Email sent to {user.email}')
        except Exception as e:
            self.stdout.write(f'Failed to send email to {user.email}: {e}')