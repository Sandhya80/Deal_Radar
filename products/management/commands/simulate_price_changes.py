from django.core.management.base import BaseCommand
from products.models import Product
import random
from decimal import Decimal

class Command(BaseCommand):
    help = 'Simulate price changes for testing email alerts'

    def handle(self, *args, **options):
        self.stdout.write('💰 Simulating price changes...')
        
        # Get all products
        products = Product.objects.all()
        
        if not products.exists():
            self.stdout.write(self.style.WARNING('⚠️ No products found. Add some products first.'))
            return
        
        updated_count = 0
        
        for product in products:
            # 40% chance of price change
            if random.random() < 0.4:
                # Price change between -25% to +15%
                change_percent = random.uniform(-0.25, 0.15)
                new_price = product.current_price * (1 + Decimal(str(change_percent)))
                
                # Ensure price doesn't go below £1
                if new_price < 1:
                    new_price = Decimal('1.00')
                
                # Round to 2 decimal places
                new_price = round(new_price, 2)
                
                old_price = product.current_price
                product.current_price = new_price
                # Optionally update product.price as well if you want to simulate both
                # product.price = new_price
                product.save()
                
                updated_count += 1
                
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