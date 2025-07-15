from django.core.management.base import BaseCommand
from products.models import Product
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Add sample products to the database'

    def handle(self, *args, **options):
        # Get or create a user for the products
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@dealradar.com',
                'is_staff': True,
                'is_superuser': True
            }
        )
        
        # Sample products data with correct field names
        sample_products = [
            {
                'name': 'Samsung Galaxy S24',
                'description': 'Latest Samsung flagship smartphone with AI features',
                'price': 799.99,
                'current_price': 799.99,
                'category': 'Electronics',
                'url': 'https://example.com/samsung-s24',
                'image_url': 'https://example.com/images/samsung-s24.jpg',
                'site_name': 'TechStore',
                'is_active': True,
                'user': user,
            },
            {
                'name': 'Nike Air Max 270',
                'description': 'Comfortable running shoes with Air Max technology',
                'price': 129.99,
                'current_price': 129.99,
                'category': 'Fashion',
                'url': 'https://example.com/nike-air-max',
                'image_url': 'https://example.com/images/nike-air-max.jpg',
                'site_name': 'SportShop',
                'is_active': True,
                'user': user,
            },
            {
                'name': 'MacBook Pro 16"',
                'description': 'Apple MacBook Pro with M3 chip for professional work',
                'price': 2499.99,
                'current_price': 2499.99,
                'category': 'Electronics',
                'url': 'https://example.com/macbook-pro',
                'image_url': 'https://example.com/images/macbook-pro.jpg',
                'site_name': 'AppleStore',
                'is_active': True,
                'user': user,
            },
            {
                'name': 'Instant Pot Duo 7-in-1',
                'description': 'Multi-functional pressure cooker for quick meals',
                'price': 89.99,
                'current_price': 89.99,
                'category': 'Home',
                'url': 'https://example.com/instant-pot',
                'image_url': 'https://example.com/images/instant-pot.jpg',
                'site_name': 'KitchenWorld',
                'is_active': True,
                'user': user,
            },
            {
                'name': 'Sony WH-1000XM5',
                'description': 'Premium noise-cancelling wireless headphones',
                'price': 349.99,
                'current_price': 349.99,
                'category': 'Electronics',
                'url': 'https://example.com/sony-headphones',
                'image_url': 'https://example.com/images/sony-headphones.jpg',
                'site_name': 'AudioHub',
                'is_active': True,
                'user': user,
            },
            {
                'name': 'Dyson V15 Detect Vacuum',
                'description': 'Advanced cordless vacuum with laser detection technology',
                'price': 649.99,
                'current_price': 649.99,
                'category': 'Home',
                'url': 'https://example.com/dyson-vacuum',
                'image_url': 'https://example.com/images/dyson-vacuum.jpg',
                'site_name': 'HomeAppliances',
                'is_active': True,
                'user': user,
            },
        ]

        # Clear existing products
        Product.objects.all().delete()
        
        # Add sample products
        for product_data in sample_products:
            try:
                product = Product.objects.create(**product_data)
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully added product: {product.name}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error adding product {product_data["name"]}: {e}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully added {len(sample_products)} sample products!')
        )