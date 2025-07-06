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
        
        for alert in active_alerts:
            checked_count += 1
            product = alert.tracked_product.product
            current_price = product.current_price
            target_price = alert.target_price
            
            # Check if current price is at or below target price
            if current_price <= target_price:
                # Trigger the alert
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