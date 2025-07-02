"""
Product Views for Deal Radar - Phase 2.5
Enhanced product display with search functionality
"""

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product
import re
from django.utils.html import format_html

def highlight_search_terms(text, search_query):
    """Highlight search terms in text"""
    if not search_query or not text:
        return text
    pattern = re.compile(f'({re.escape(search_query)})', re.IGNORECASE)
    highlighted = pattern.sub(r'<mark style="background-color: #ffeb3b; padding: 2px 4px; border-radius: 3px;">\1</mark>', str(text))
    return format_html(highlighted)

def home(request):
    """Phase 2.5: Enhanced homepage with search"""
    search_query = request.GET.get('search', '').strip()
    
    if search_query:
        products = Product.objects.filter(
            Q(name__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(site_name__icontains=search_query) |
            Q(description__icontains=search_query)
        ).order_by('-created_at')
    else:
        products = Product.objects.all().order_by('-created_at')
    
    total_products = Product.objects.count()
    
    context = {
        'products': products,
        'total_products': total_products,
        'search_query': search_query,
        'search_count': products.count(),
        'highlight_search_terms': highlight_search_terms,
    }
    
    return render(request, 'products/home.html', context)

def product_detail(request, pk):
    """Enhanced product detail page"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})
