"""
Management command to simulate random price changes for all products.

This is useful for testing price drop detection, alert logic, and dashboard updates
without needing real-time scraping. It randomly adjusts product prices up or down.

Usage:
    python manage.py simulate_price_changes
"""

from django.core.management.base import BaseCommand
from products.models import Product
import random
from decimal import Decimal

class Command(BaseCommand):
    help = 'Simulate price changes for testing email alerts'

    def handle(self, *args, **options):
        self.stdout.write('💰 Simulating price changes...')

        # Fetch all products from the database
        products = Product.objects.all()

        if not products.exists():
            self.stdout.write(self.style.WARNING('⚠️ No products found. Add some products first.'))
            return

        updated_count = 0

        # Iterate through each product and randomly change its price
        for product in products:
            # 40% chance to change the price
            if random.random() < 0.4:
                # Random price change between -25% and +15%
                change_percent = random.uniform(-0.25, 0.15)
                new_price = product.current_price * (1 + Decimal(str(change_percent)))

                # Ensure price doesn't go below £1
                if new_price < 1:
                    new_price = Decimal('1.00')

                # Round to 2 decimal places for currency
                new_price = round(new_price, 2)

                old_price = product.current_price
                product.current_price = new_price
                # Optionally update product.price as well if needed
                # product.price = new_price
                product.save()

                updated_count += 1

                # Output whether the price dropped or increased
                if new_price < old_price:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'📉 {product.name}: £{old_price} → £{new_price} (Price DROP)'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f'📈 {product.name}: £{old_price} → £{new_price} (Price UP)'
                        )
                    )

        self.stdout.write(f'📊 {updated_count} out of {products.count()} products updated')

        if updated_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'💰 Price simulation completed! Run check_price_alerts next.')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️ No prices changed this time. Try running again.')
            )