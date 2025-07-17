"""
Management command to check all active price alerts and send notifications if triggered.

This command scans all enabled, non-triggered PriceAlert objects. If the current price
of a tracked product is at or below the user's target price, it triggers the alert
and sends an email notification.

Usage:
    python manage.py check_price_alerts
"""

from django.core.management.base import BaseCommand
from products.models import PriceAlert
from django.utils import timezone

class Command(BaseCommand):
    help = 'Check price alerts and send email notifications'

    def handle(self, *args, **options):
        self.stdout.write('🔍 Checking price alerts...')

        # Get all enabled, non-triggered alerts
        active_alerts = PriceAlert.objects.filter(
            is_enabled=True,
            is_triggered=False
        ).select_related('tracked_product__product', 'tracked_product__user')

        triggered_count = 0
        checked_count = 0

        # Check each alert for price drop condition
        for alert in active_alerts:
            checked_count += 1
            product = alert.tracked_product.product
            current_price = product.current_price
            target_price = alert.target_price

            # Trigger alert if current price is at or below target price
            if current_price <= target_price:
                # Calls alert.trigger_alert(), which sends notification and marks as triggered
                if alert.trigger_alert(current_price):
                    triggered_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ Alert triggered: {product.name} '
                            f'(£{current_price} <= £{target_price})'
                        )
                    )

        self.stdout.write(f'📊 Checked {checked_count} alerts')

        if triggered_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'🎯 {triggered_count} price alerts triggered and emails sent!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️ No price alerts triggered.')
            )

        self.stdout.write('✅ Price alert check completed.')