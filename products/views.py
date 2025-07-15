from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from .models import Product, TrackedProduct, UserProfile, PriceAlert
import re
from django.utils.html import format_html
import csv
import io
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
from django.urls import reverse
import logging
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
import stripe

from .email_utils import send_welcome_email  # Import the email utility
from .scraper import scrape_product_data

stripe.api_key = settings.STRIPE_SECRET_KEY

logger = logging.getLogger(__name__)

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
        logger.info(f"User searched for '{search_query}' - {products.count()} results found.")
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
    user = request.user
    
    tracked_products = TrackedProduct.objects.filter(user=user, is_active=True).select_related('product')
    total_tracked = tracked_products.count()
    active_alerts = PriceAlert.objects.filter(
        tracked_product__user=user, 
        is_enabled=True
    ).count()
    triggered_alerts = PriceAlert.objects.filter(
        tracked_product__user=user, 
        is_triggered=True
    ).count()
    total_savings = 0
    triggered_alert_list = PriceAlert.objects.filter(
        tracked_product__user=user, 
        is_triggered=True
    ).select_related('tracked_product__product')
    for alert in triggered_alert_list:
        current_price = alert.tracked_product.product.current_price
        target_price = alert.target_price
        if current_price and target_price and current_price < target_price:
            savings = target_price - current_price
            total_savings += savings
    recent_alerts = triggered_alert_list.order_by('-triggered_at')[:5]
    context = {
        'total_tracked': total_tracked,
        'total_alerts': active_alerts,
        'triggered_alerts': triggered_alerts,
        'total_savings': total_savings,
        'tracked_products': tracked_products,
        'recent_alerts': recent_alerts,
        'user': user,
    }
    logger.debug(f"Dashboard loaded for user {user.username}: {total_tracked} tracked, {active_alerts} active alerts.")
    return render(request, 'products/dashboard.html', context)

@login_required 
def add_to_tracking(request, pk):
    user_profile = request.user.userprofile
    plan = settings.STRIPE_PLANS[user_profile.subscription_plan]
    product_limit = plan['product_limit']
    active_tracked_count = request.user.tracked_products.filter(is_active=True).count()

    if product_limit is not None and active_tracked_count >= product_limit:
        messages.error(request, f"You have reached your product limit ({product_limit}) for your current plan. Upgrade to track more products.")
        return redirect('dashboard')

    product = get_object_or_404(Product, pk=pk)
    tracked_product, created = TrackedProduct.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'is_active': True}
    )
    if created:
        messages.success(request, f'Added "{product.name}" to your tracking list!')
        logger.info(f'User {request.user.username} started tracking product "{product.name}".')
    else:
        if not tracked_product.is_active:
            tracked_product.is_active = True
            tracked_product.save()
            messages.success(request, f'Re-activated tracking for "{product.name}"!')
            logger.info(f'User {request.user.username} re-activated tracking for "{product.name}".')
        else:
            messages.info(request, f'"{product.name}" is already in your tracking list.')
            logger.info(f'User {request.user.username} tried to add already tracked product "{product.name}".')
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
        logger.info(f'User {request.user.username} removed product "{product.name}" from tracking.')
    except TrackedProduct.DoesNotExist:
        messages.error(request, 'Product not found in your tracking list.')
        logger.warning(f'User {request.user.username} tried to remove non-tracked product "{product.name}".')
    return redirect('product_detail', pk=pk)

def signup(request):
    """Phase 3: User registration with welcome email"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            send_welcome_email(user)
            logger.info(f"New user signed up: {user.username} ({user.email})")
            messages.success(request, 'Welcome to Deal Radar! Check your email for getting started tips.')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def create_price_alert(request, pk):
    """Create a price alert for a tracked product"""
    tracked_product = get_object_or_404(TrackedProduct, pk=pk, user=request.user)
    if request.method == 'POST':
        target_price = request.POST.get('target_price')
        if target_price:
            try:
                target_price = float(target_price)
                if target_price <= 0:
                    messages.error(request, 'Target price must be greater than 0.')
                    logger.warning(f"User {request.user.username} entered invalid target price: {target_price}")
                    return redirect('dashboard')
                alert, created = PriceAlert.objects.get_or_create(
                    tracked_product=tracked_product,
                    target_price=target_price,
                    defaults={'is_enabled': True, 'is_triggered': False}
                )
                if created:
                    messages.success(request, f'Price alert set for £{target_price}! You\'ll be notified when the price drops.')
                    logger.info(f"User {request.user.username} set new price alert for {tracked_product.product.name} at £{target_price}")
                else:
                    messages.info(request, f'Price alert for £{target_price} already exists.')
                    logger.info(f"User {request.user.username} tried to set duplicate price alert for {tracked_product.product.name} at £{target_price}")
            except ValueError:
                messages.error(request, 'Please enter a valid price.')
                logger.warning(f"User {request.user.username} entered non-numeric target price: {target_price}")
        else:
            messages.error(request, 'Please enter a target price.')
            logger.warning(f"User {request.user.username} submitted empty target price.")
    return redirect('dashboard')

@login_required
def toggle_price_alert(request, pk):
    """Toggle price alert on/off"""
    alert = get_object_or_404(PriceAlert, pk=pk, tracked_product__user=request.user)
    alert.is_enabled = not alert.is_enabled
    alert.save()
    status = "enabled" if alert.is_enabled else "disabled"
    messages.success(request, f'Price alert for "{alert.tracked_product.product.name}" {status}.')
    logger.info(f"User {request.user.username} {status} price alert for {alert.tracked_product.product.name}.")
    return redirect('dashboard')

@login_required
def delete_price_alert(request, pk):
    """Delete a price alert"""
    alert = get_object_or_404(PriceAlert, pk=pk, tracked_product__user=request.user)
    product_name = alert.tracked_product.product.name
    alert.delete()
    messages.success(request, f'Price alert for "{product_name}" deleted.')
    logger.info(f"User {request.user.username} deleted price alert for {product_name}.")
    return redirect('dashboard')

@login_required
def reset_price_alert(request, pk):
    """Reset a triggered price alert"""
    alert = get_object_or_404(PriceAlert, pk=pk, tracked_product__user=request.user)
    alert.is_triggered = False
    alert.triggered_at = None
    alert.save()
    messages.success(request, f'Price alert for "{alert.tracked_product.product.name}" reset and reactivated.')
    logger.info(f"User {request.user.username} reset price alert for {alert.tracked_product.product.name}.")
    return redirect('dashboard')

@login_required
def profile(request):
    """User profile management page"""
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name = request.POST.get('last_name', '').strip()
        user.email = request.POST.get('email', '').strip()
        user.save()
        profile.email_notifications = request.POST.get('email_notifications') == 'on'
        profile.whatsapp_notifications = request.POST.get('whatsapp_notifications') == 'on'
        profile.whatsapp_number = request.POST.get('whatsapp_number', '').strip()
        profile.notification_frequency = request.POST.get('notification_frequency', 'instant')
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        logger.info(f"User {user.username} updated profile preferences.")
        return redirect('profile')
    context = {
        'user': user,
        'profile': profile,
        'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
    }
    return render(request, 'products/profile.html', context)

@login_required
def user_settings(request):
    """Settings page for user preferences"""
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    if request.method == 'POST':
        if 'update_email' in request.POST:
            profile.email_notifications = request.POST.get('email_notifications') == 'on'
            profile.notification_frequency = request.POST.get('notification_frequency', 'instant')
            profile.save()
            messages.success(request, 'Email settings updated successfully!')
            logger.info(f"User {user.username} updated email settings.")
            return redirect('settings')
        elif 'clear_data' in request.POST:
            TrackedProduct.objects.filter(user=user).delete()
            PriceAlert.objects.filter(tracked_product__user=user).delete()
            messages.success(request, 'All data cleared successfully!')
            logger.info(f"User {user.username} cleared all tracked products and alerts.")
            return redirect('settings')
    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'products/settings.html', context)

@login_required
def export_data(request):
    """Export user data to Excel CSV"""
    user = request.user
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="deal_radar_data_{user.username}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Product Name', 'URL', 'Current Price', 'Target Price', 'Site', 'Category', 'Date Added'])
    tracked_products = TrackedProduct.objects.filter(user=user).select_related('product')
    for tracked in tracked_products:
        writer.writerow([
            tracked.product.name,
            tracked.product.url,
            tracked.product.current_price,
            tracked.target_price,
            tracked.product.site_name,
            tracked.product.category,
            tracked.created_at.strftime('%Y-%m-%d')
        ])
    logger.info(f"User {user.username} exported data as CSV.")
    return response

@login_required
def export_json(request):
    """Export user data to JSON"""
    user = request.user
    tracked_products = TrackedProduct.objects.filter(user=user).select_related('product')
    data = {
        'user': user.username,
        'exported_at': timezone.now().isoformat(),
        'tracked_products': []
    }
    for tracked in tracked_products:
        data['tracked_products'].append({
            'product_name': tracked.product.name,
            'url': tracked.product.url,
            'current_price': float(tracked.product.current_price),
            'target_price': float(tracked.target_price) if tracked.target_price else None,
            'site_name': tracked.product.site_name,
            'category': tracked.product.category,
            'date_added': tracked.created_at.isoformat()
        })
    response = JsonResponse(data, indent=2)
    response['Content-Disposition'] = f'attachment; filename="deal_radar_data_{user.username}.json"'
    logger.info(f"User {user.username} exported data as JSON.")
    return response

@login_required
def delete_account(request):
    """Delete user account"""
    if request.method == 'POST':
        user = request.user
        logout(request)
        username = user.username
        user.delete()
        messages.success(request, "Your account has been deleted.")
        logger.warning(f"User {username} deleted their account.")
        return redirect('home')
    return render(request, 'registration/delete_account_confirm.html')

def category_products(request, slug):
    category_dict = dict(Product.CATEGORY_CHOICES)
    category_name = category_dict.get(slug, slug)
    products = Product.objects.filter(category=slug)
    logger.info(f"Category page viewed: {category_name} ({slug})")
    return render(request, 'products/category_products.html', {
        'category': {'slug': slug, 'name': category_name},
        'products': products,
    })

@login_required
def add_product(request):
    """Phase 3.1: Add product page with category selection and improved UX"""
    user_profile = request.user.userprofile
    plan = settings.STRIPE_PLANS[user_profile.subscription_plan]
    product_limit = plan['product_limit']

    # Count active tracked products for this user
    active_tracked_count = request.user.tracked_products.filter(is_active=True).count()

    if product_limit is not None and active_tracked_count >= product_limit:
        messages.error(request, f"You have reached your product limit ({product_limit}) for your current plan. Upgrade to track more products.")
        return redirect('dashboard')

    if request.method == 'POST':
        existing_product_id = request.POST.get('existing_product')
        product_url = request.POST.get('product_url')
        target_price = request.POST.get('target_price')
        category = request.POST.get('category')

        if not existing_product_id and not product_url:
            messages.error(request, "Please provide a product URL or select an existing product.")
            return redirect('add_product')

        if existing_product_id:
            # User selected an existing product
            try:
                product = Product.objects.get(id=existing_product_id)
            except Product.DoesNotExist:
                messages.error(request, "Selected product does not exist.")
                return redirect('add_product')
        elif product_url:
            # User entered a new product URL
            # (You may want to validate and create the product here)
            product, created = Product.objects.get_or_create(
                url=product_url,
                defaults={'category': category}
            )
        else:
            messages.error(request, "Please provide a product URL or select an existing product.")
            return redirect('add_product')

        # Now create the tracked product (or alert) for this user
        TrackedProduct.objects.create(
            user=request.user,
            product=product,
            target_price=target_price,
            is_active=True
        )
        messages.success(request, "Product added to your tracking list!")
        return redirect('dashboard')

    categories = Product.CATEGORY_CHOICES
    products_by_category = {}
    for key, _ in categories:
        products_by_category[key] = list(Product.objects.filter(category=key).values('id', 'name'))

    context = {
        'categories': categories,
        'products_by_category_json': json.dumps(products_by_category, cls=DjangoJSONEncoder),
    }
    return render(request, 'products/add_product.html', context)

@csrf_exempt
def request_site_support(request):
    if request.method == 'POST':
        site_url = request.POST.get('site_url')
        # You can save this to a model or send an email to admin
        messages.success(request, "Thank you! We'll review your request soon.")
        logger.info(f"Site support requested for: {site_url}")
        return redirect('add_product')
    return render(request, 'products/request_site_support.html')

@login_required
def create_checkout_session(request, plan_key):
    plan = settings.STRIPE_PLANS.get(plan_key)
    if not plan or not plan['price_id']:
        return HttpResponseBadRequest("Invalid plan selected.")

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': plan['price_id'],
            'quantity': 1,
        }],
        mode='subscription',
        customer_email=request.user.email,
        success_url=settings.SITE_DOMAIN + '/subscription/success/',
        cancel_url=settings.SITE_DOMAIN + '/subscription/cancel/',
    )
    return JsonResponse({'sessionId': checkout_session.id})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session.get('customer_email')
        subscription_id = session.get('subscription')
        customer_id = session.get('customer')
        session_id = session.get('id')

        # Fetch line items to get the price_id
        try:
            line_items = stripe.checkout.Session.list_line_items(session_id, limit=1)
            price_id = line_items['data'][0]['price']['id']
        except Exception:
            price_id = None

        # Map price_id to plan_key
        plan_key = None
        for key, plan in settings.STRIPE_PLANS.items():
            if plan.get('price_id') == price_id:
                plan_key = key
                break

        from django.contrib.auth import get_user_model
        User = get_user_model()
        try:
            user = User.objects.get(email=customer_email)
            profile = user.userprofile
            if plan_key:
                profile.subscription_plan = plan_key
            profile.stripe_customer_id = customer_id
            profile.stripe_subscription_id = subscription_id
            profile.subscription_status = 'active'
            profile.save()
        except User.DoesNotExist:
            pass

    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        customer_id = subscription['customer']
        status = subscription['status']
        # Update UserProfile with new status
        from .models import UserProfile
        try:
            profile = UserProfile.objects.get(stripe_customer_id=customer_id)
            profile.subscription_status = status
            profile.save()
        except UserProfile.DoesNotExist:
            pass

    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        customer_id = subscription['customer']
        # Mark subscription as canceled
        from .models import UserProfile
        try:
            profile = UserProfile.objects.get(stripe_customer_id=customer_id)
            profile.subscription_status = 'canceled'
            profile.subscription_plan = 'free'
            profile.save()
        except UserProfile.DoesNotExist:
            pass

    # Add more event types as needed

    return HttpResponse(status=200)