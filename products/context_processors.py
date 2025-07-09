from .models import Product

def product_category_choices(request):
    return {'product_category_choices': Product.CATEGORY_CHOICES}