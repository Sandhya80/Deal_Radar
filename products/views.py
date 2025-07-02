"""
Product Views for Deal Radar - Phase 3.1
User authentication and personal tracking (SQLite-based)
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Product, TrackedProduct, UserProfile, PriceAlert
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
    """Phase 3: Enhanced homepage with user context"""
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
    
    # Get user's tracked products if logged in
    user_tracked_products = []
    if request.user.is_authenticated:
        user_tracked_products = TrackedProduct.objects.filter(
            user=request.user, is_active=True
        ).values_list('product_id', flat=True)
    
    context = {
        'products': products,
        'total_products': Product.objects.count(),
        'search_query': search_query,
        'search_count': products.count(),
        'highlight_search_terms': highlight_search_terms,
        'user_tracked_products': list(user_tracked_products),
    }
    
    return render(request, 'products/home.html', context)

def product_detail(request, pk):
    """Phase 3: Enhanced product detail with tracking option"""
    product = get_object_or_404(Product, pk=pk)
    
    is_tracked = False
    tracked_product = None
    
    if request.user.is_authenticated:
        try:
            tracked_product = TrackedProduct.objects.get(
                user=request.user, 
                product=product, 
                is_active=True
            )
            is_tracked = True
        except TrackedProduct.DoesNotExist:
            pass
    
    context = {
        'product': product,
        'is_tracked': is_tracked,
        'tracked_product': tracked_product,
    }
    
    return render(request, 'products/product_detail.html', context)

@login_required
def dashboard(request):
    """Phase 3: User's personal dashboard"""
    user_tracked = TrackedProduct.objects.filter(
        user=request.user, 
        is_active=True
    ).select_related('product').order_by('-added_at')
    
    total_tracked = user_tracked.count()
    total_alerts = PriceAlert.objects.filter(
        tracked_product__user=request.user,
        is_enabled=True
    ).count()
    
    context = {
        'tracked_products': user_tracked,
        'total_tracked': total_tracked,
        'total_alerts': total_alerts,
    }
    
    return render(request, 'products/dashboard.html', context)

@login_required 
def add_to_tracking(request, pk):
    """Phase 3: Add product to user's tracking list"""
    product = get_object_or_404(Product, pk=pk)
    
    tracked_product, created = TrackedProduct.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'is_active': True}
    )
    
    if created:
        messages.success(request, f'Added "{product.name}" to your tracking list!')
    else:
        if not tracked_product.is_active:
            tracked_product.is_active = True
            tracked_product.save()
            messages.success(request, f'Re-activated tracking for "{product.name}"!')
        else:
            messages.info(request, f'"{product.name}" is already in your tracking list.')
    
    return redirect('product_detail', pk=pk)

@login_required
def remove_from_tracking(request, pk):
    """Phase 3: Remove product from user's tracking list"""  
    product = get_object_or_404(Product, pk=pk)
    
    try:
        tracked_product = TrackedProduct.objects.get(
            user=request.user, 
            product=product, 
            is_active=True
        )
        tracked_product.is_active = False
        tracked_product.save()
        messages.success(request, f'Removed "{product.name}" from your tracking list.')
    except TrackedProduct.DoesNotExist:
        messages.error(request, 'Product not found in your tracking list.')
    
    return redirect('product_detail', pk=pk)

def signup(request):
    """Phase 3: User registration"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Welcome to Deal Radar! Your account has been created.')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})
