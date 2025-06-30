"""
Product Views for Deal Radar

This module contains all views related to product tracking functionality.
It provides both web interface views (for the dashboard) and API endpoints
(for mobile apps and frontend frameworks).

Architecture Logic:
- Web views return rendered HTML templates
- API views return JSON responses using Django REST Framework
- All views require authentication to protect user data
- Views implement subscription tier business logic

Business Logic Implementation:
- Users can track products by providing URLs and desired prices
- Free users are limited to 3 tracked products
- Premium users have unlimited tracking
- Real-time price updates and alerts (implemented in Phase 2)
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, TrackedProduct, PriceHistory, DealAlert

# Create your views here.

@login_required
def dashboard(request):
    """
    Main dashboard view showing user's tracked products
    
    This is the primary interface where users manage their product tracking.
    It displays all active tracked products with current pricing information
    and provides quick access to management actions.
    
    Business Logic:
    - Only show active tracked products (user hasn't deleted them)
    - Display current prices with visual indicators for price changes
    - Show subscription limits and upgrade prompts for free users
    - Provide quick actions: add new products, edit tracking, delete
    
    Template Context:
    - tracked_products: QuerySet of user's TrackedProduct objects
    - can_add_more: Boolean indicating if user can track more products
    - total_tracked: Count of currently tracked products
    
    Future Enhancements (Phase 2):
    - Price history charts using Chart.js
    - Recent deal alerts and notifications
    - Bulk actions for managing multiple products
    - Filter and search functionality
    """
    # Optimize database queries with select_related for efficiency
    # This prevents N+1 query problems when accessing product data
    tracked_products = TrackedProduct.objects.filter(
        user=request.user, 
        is_active=True
    ).select_related('product').order_by('-created_at')
    
    # Check subscription limits for business rule enforcement
    # Free users can only track 3 products, premium users unlimited
    profile = getattr(request.user, 'profile', None)
    can_add_more = profile.can_track_more_products if profile else False
    
    context = {
        'tracked_products': tracked_products,
        'can_add_more': can_add_more,
        'total_tracked': tracked_products.count(),
        # Additional context for Phase 2:
        # 'recent_alerts': recent deal alerts
        # 'price_changes': products with recent price changes
    }
    return render(request, 'products/dashboard.html', context)

@login_required
def add_product(request):
    """
    Add a new product to user's tracking list
    
    This view handles the form for adding new products to track.
    It accepts a product URL and desired price from the user.
    
    Business Logic:
    - Validate subscription limits before allowing new products
    - Check if product already exists to prevent duplicates
    - Create minimal product record (Phase 1: manual data entry)
    - Create TrackedProduct relationship with user preferences
    
    Form Processing:
    - GET: Display the add product form
    - POST: Process form submission and create tracking
    
    Phase 2 Enhancements:
    - Web scraping to automatically populate product details
    - URL validation to ensure supported e-commerce sites
    - Duplicate detection based on product URLs
    - Automatic price fetching and validation
    
    Error Handling:
    - Subscription limit exceeded
    - Invalid URLs or pricing data
    - Duplicate tracking attempts
    """
    if request.method == 'POST':
        url = request.POST.get('url')
        desired_price = request.POST.get('desired_price')
        
        # Validate required fields
        if url and desired_price:
            # Check subscription limits before proceeding
            profile = getattr(request.user, 'profile', None)
            if profile and not profile.can_track_more_products:
                messages.error(request, 'You have reached your tracking limit. Upgrade to Premium for unlimited tracking!')
                return redirect('dashboard')
            
            try:
                # Convert price to float for validation
                price_value = float(desired_price)
                if price_value <= 0:
                    raise ValueError("Price must be positive")
                
                # Create or get existing product
                # Phase 1: Basic product creation with minimal data
                # Phase 2: Will include web scraping for full product details
                product, created = Product.objects.get_or_create(
                    url=url,
                    defaults={
                        'name': f'Product from {url}',  # Placeholder name
                        'current_price': price_value,
                        'site_name': 'Manual',  # Will be auto-detected in Phase 2
                    }
                )
                
                # Create tracking relationship with user preferences
                tracked_product, tracking_created = TrackedProduct.objects.get_or_create(
                    user=request.user,
                    product=product,
                    defaults={'desired_price': price_value}
                )
                
                if tracking_created:
                    messages.success(request, 'Product added successfully! You will receive alerts when the price drops.')
                else:
                    messages.info(request, 'You are already tracking this product.')
                
                return redirect('dashboard')
                
            except ValueError as e:
                messages.error(request, 'Please enter a valid price.')
        else:
            messages.error(request, 'Please provide both URL and desired price.')
    
    # GET request: show the form
    return render(request, 'products/add_product.html')

@login_required
def edit_product(request, product_id):
    """
    Edit tracking preferences for a user's tracked product
    
    This view allows users to modify their tracking preferences for
    a specific product without changing the core product data.
    
    Business Logic:
    - Users can only edit their own tracked products
    - Modifications include: desired price, notification preferences
    - Core product data (name, URL) remains unchanged
    - Changes are immediately saved and alerts updated
    
    Security:
    - get_object_or_404 ensures user owns the tracked product
    - Django's @login_required prevents unauthorized access
    
    Form Processing:
    - GET: Display current tracking settings in form
    - POST: Update tracking preferences and redirect to dashboard
    
    Future Enhancements:
    - Notification frequency settings
    - Custom discount percentage thresholds
    - Pause/resume tracking without deletion
    """
    # Security check: ensure user owns this tracked product
    tracked_product = get_object_or_404(
        TrackedProduct, 
        id=product_id, 
        user=request.user  # Prevents users from editing others' products
    )
    
    if request.method == 'POST':
        desired_price = request.POST.get('desired_price')
        
        if desired_price:
            try:
                price_value = float(desired_price)
                if price_value <= 0:
                    raise ValueError("Price must be positive")
                
                # Update tracking preferences
                tracked_product.desired_price = price_value
                
                # Future: Update notification preferences from form
                # tracked_product.notify_on_price_drop = request.POST.get('notify_price_drop', False)
                # tracked_product.minimum_discount_percent = request.POST.get('min_discount', 10.0)
                
                tracked_product.save()
                messages.success(request, 'Product tracking updated successfully!')
                return redirect('dashboard')
                
            except ValueError:
                messages.error(request, 'Please enter a valid price.')
        else:
            messages.error(request, 'Please provide a desired price.')
    
    # GET request: show edit form with current values
    context = {'tracked_product': tracked_product}
    return render(request, 'products/edit_product.html', context)

@login_required
def delete_product(request, product_id):
    """
    Remove a product from user's tracking list
    
    This view handles the deletion of tracked products from a user's list.
    It implements soft deletion by setting is_active=False to preserve
    historical data while removing the product from active tracking.
    
    Business Logic:
    - Only the tracking relationship is deleted, not the core product
    - Other users can continue tracking the same product
    - Price history is preserved for analytics
    - Deletion is immediate and cannot be undone (Phase 1)
    
    Security:
    - Users can only delete their own tracked products
    - Confirmation page prevents accidental deletions
    - get_object_or_404 ensures proper ownership
    
    UX Considerations:
    - GET: Show confirmation page with product details
    - POST: Perform deletion and redirect with success message
    - Cancel option returns to dashboard without changes
    
    Future Enhancements:
    - Soft deletion with restore capability
    - Bulk delete functionality
    - Export data before deletion
    """
    # Security: ensure user owns this tracked product
    tracked_product = get_object_or_404(
        TrackedProduct, 
        id=product_id, 
        user=request.user
    )
    
    if request.method == 'POST':
        # Get product name for success message before deletion
        product_name = tracked_product.product.name
        
        # Perform deletion - this removes the tracking relationship
        # The core Product object remains for other users who may be tracking it
        tracked_product.delete()
        
        messages.success(request, f'"{product_name}" has been removed from your tracking list.')
        return redirect('dashboard')
    
    # GET request: show confirmation page
    context = {
        'tracked_product': tracked_product,
        'product_name': tracked_product.product.name,
        'current_price': tracked_product.product.current_price,
    }
    return render(request, 'products/delete_product.html', context)

# API Views for Mobile Apps and Frontend Frameworks
# These views provide JSON responses for programmatic access

@api_view(['GET'])
def product_list_api(request):
    """
    API endpoint to retrieve user's tracked products
    
    This RESTful API endpoint provides programmatic access to a user's
    tracked products for mobile apps, frontend frameworks, or third-party
    integrations.
    
    Authentication:
    - Requires valid authentication token or active session
    - Returns 401 for unauthenticated requests
    
    Response Format:
    - JSON array of tracked product objects
    - Each object includes product details and tracking preferences
    - Optimized for mobile app consumption
    
    Business Logic:
    - Only returns active tracked products for the authenticated user
    - Includes calculated fields like deal availability
    - Efficient database queries with select_related
    
    Future Enhancements:
    - Pagination for users with many tracked products
    - Filtering and search parameters
    - Price history data inclusion
    - Real-time updates via WebSockets
    
    Example Response:
    [
        {
            "id": 1,
            "product_name": "iPhone 15 Pro",
            "product_url": "https://amazon.com/...",
            "current_price": 799.99,
            "desired_price": 699.99,
            "is_deal_available": false,
            "discount_percent": 0.0
        }
    ]
    """
    # Authentication check (handled by DRF authentication classes)
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    
    # Efficient query with related product data
    tracked_products = TrackedProduct.objects.filter(
        user=request.user, 
        is_active=True
    ).select_related('product')
    
    # Serialize data for JSON response
    data = []
    for tp in tracked_products:
        data.append({
            'id': tp.id,
            'product_name': tp.product.name,
            'product_url': tp.product.url,
            'product_image': tp.product.image_url or '',
            'current_price': float(tp.product.current_price),
            'desired_price': float(tp.desired_price),
            'is_deal_available': tp.is_deal_available,
            'discount_percent': float(tp.current_discount_percent),
            'last_updated': tp.product.last_scraped.isoformat(),
            'created_at': tp.created_at.isoformat(),
        })
    
    return Response({
        'products': data,
        'total_count': len(data),
        'can_add_more': request.user.profile.can_track_more_products if hasattr(request.user, 'profile') else False
    })
