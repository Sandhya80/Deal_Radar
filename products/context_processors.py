# Context processor to inject product category choices into all templates.

from .models import Product

def product_category_choices(request):
    """
    Returns a dictionary of product category choices for use in templates.
    """
    return {'product_category_choices': Product.CATEGORY_CHOICES}