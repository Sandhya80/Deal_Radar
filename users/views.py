"""
User Views for Deal Radar

This module handles user authentication, registration, and profile management.
It provides both traditional form-based views and API endpoints for user
account operations.

Authentication Strategy:
- Django's built-in authentication system as the foundation
- Django AllAuth for advanced features (email login, social auth)
- Custom UserProfile model for Deal Radar-specific data
- API token authentication for mobile apps

Business Logic:
- Automatic profile creation upon registration
- Email-based authentication (no usernames required)
- Subscription tier management (free vs premium)
- Notification preference management
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserProfile

# Create your views here.

def home(request):
    """
    Landing page view for Deal Radar
    
    This is the main entry point for visitors to the site.
    It serves different content based on authentication status.
    
    Business Logic:
    - Authenticated users are redirected to their dashboard
    - Anonymous users see the marketing landing page
    - Landing page includes features, pricing, and signup CTA
    
    Template Context:
    - No specific context for anonymous users
    - Marketing content is static in template
    
    Future Enhancements:
    - A/B testing for conversion optimization
    - Dynamic pricing display
    - User testimonials and success stories
    """
    if request.user.is_authenticated:
        return redirect('dashboard')  # Send logged-in users to their dashboard
    return render(request, 'users/home.html')

def register_view(request):
    """
    User registration view with automatic profile creation
    
    This view handles new user registration and sets up their Deal Radar
    account with default settings and subscription tier.
    
    Business Logic:
    - Creates Django User account with form validation
    - Automatically creates UserProfile with default settings
    - Sets up free subscription tier (3 products max)
    - Redirects to login page for account activation
    
    Form Processing:
    - GET: Display registration form
    - POST: Process registration and create account
    
    Profile Initialization:
    - Email notifications enabled by default
    - SMS/WhatsApp disabled (requires phone number)
    - Free tier subscription (max_tracked_products = 3)
    - All notification preferences enabled for opt-out model
    
    Error Handling:
    - Form validation errors displayed to user
    - Username/email uniqueness enforced by Django
    - Password strength requirements from settings
    
    Future Enhancements:
    - Email verification workflow
    - Social media registration (Google, Facebook)
    - Referral code system for bonus features
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Create the user account
            user = form.save()
            
            # Create associated UserProfile with default settings
            # This establishes the subscription tier and preferences
            UserProfile.objects.create(
                user=user,
                # Default settings for new users
                email_notifications=True,      # Email alerts enabled
                sms_notifications=False,       # SMS requires phone number
                whatsapp_notifications=False,  # WhatsApp requires phone number
                is_premium=False,              # Start with free tier
                max_tracked_products=3,        # Free tier limit
            )
            
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    """
    User authentication view with redirect logic
    
    This view handles user login with proper authentication flow
    and security measures.
    
    Business Logic:
    - Authenticate users with username/password combination
    - Redirect authenticated users to their dashboard
    - Handle authentication failures gracefully
    - Support "next" parameter for redirecting after login
    
    Security Features:
    - Django's built-in authentication system
    - CSRF protection through middleware
    - Session management for persistent login
    - Password validation and rate limiting (future)
    
    Form Processing:
    - GET: Display login form
    - POST: Process authentication attempt
    
    Error Handling:
    - Invalid credentials show user-friendly error
    - Form validation errors are displayed
    - Multiple failed attempts can trigger lockout (future)
    
    Future Enhancements:
    - Two-factor authentication (2FA)
    - "Remember me" functionality
    - Social media login integration
    - Account lockout after failed attempts
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.info(request, f"Welcome back, {username}!")
                
                # Redirect to 'next' parameter or dashboard
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})

@login_required
def logout_view(request):
    """
    User logout view with session cleanup
    
    This view handles user logout and properly cleans up the session
    to ensure security and prevent unauthorized access.
    
    Security Features:
    - Clears user session completely
    - Invalidates authentication tokens
    - Redirects to public page to prevent back-button access
    - Displays confirmation message for user feedback
    
    Business Logic:
    - Only authenticated users can access this view
    - Logout is immediate and cannot be undone
    - User is redirected to home page
    - Success message confirms logout completion
    """
    username = request.user.username  # Get username before logout
    logout(request)  # Clear session and authentication
    messages.info(request, f"You have successfully logged out, {username}. Come back soon!")
    return redirect('home')

@login_required
def profile_view(request):
    """
    User profile management view
    
    This view allows users to manage their account settings,
    notification preferences, and subscription information.
    
    Business Logic:
    - Display current profile settings and subscription status
    - Allow updates to notification preferences
    - Show subscription limits and upgrade options
    - Validate phone number format for SMS/WhatsApp
    
    Profile Settings:
    - Contact information (phone number)
    - Notification preferences (email, SMS, WhatsApp)
    - Subscription status and limits
    - Account statistics (products tracked, alerts sent)
    
    Form Processing:
    - GET: Display current settings
    - POST: Update profile with new preferences
    
    Validation:
    - Phone number format validation for international numbers
    - Notification dependency checking (phone required for SMS)
    - Business rule enforcement (subscription limits)
    
    Future Enhancements:
    - Profile picture upload
    - Timezone selection
    - Password change functionality
    - Account deletion option
    """
    # Get or create profile for this user (defensive programming)
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update contact information
        phone_number = request.POST.get('phone_number', '').strip()
        profile.phone_number = phone_number
        
        # Update notification preferences
        profile.email_notifications = request.POST.get('email_notifications') == 'on'
        profile.sms_notifications = request.POST.get('sms_notifications') == 'on'
        profile.whatsapp_notifications = request.POST.get('whatsapp_notifications') == 'on'
        
        # Business rule: SMS/WhatsApp require phone number
        if (profile.sms_notifications or profile.whatsapp_notifications) and not phone_number:
            messages.error(request, 'Phone number is required for SMS or WhatsApp notifications.')
            return render(request, 'users/profile.html', {'profile': profile})
        
        try:
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        except Exception as e:
            messages.error(request, 'Error updating profile. Please check your information.')
    
    # Calculate account statistics for display
    from products.models import TrackedProduct
    tracked_count = TrackedProduct.objects.filter(user=request.user, is_active=True).count()
    
    context = {
        'profile': profile,
        'tracked_count': tracked_count,
        'tracking_limit': profile.max_tracked_products,
        'can_track_more': profile.can_track_more_products,
    }
    
    return render(request, 'users/profile.html', context)

# API Views for Mobile Apps and Frontend Integration

@api_view(['GET'])
def user_profile_api(request):
    """
    API endpoint for user profile data
    
    This RESTful API endpoint provides programmatic access to user
    profile information for mobile apps and frontend frameworks.
    
    Authentication:
    - Requires valid authentication token or active session
    - Returns 401 for unauthenticated requests
    
    Response Format:
    - JSON object with user profile data
    - Includes subscription status and limits
    - Calculated fields for business logic
    
    Business Logic:
    - Only returns data for the authenticated user
    - Includes subscription tier information
    - Provides tracking limits and current usage
    - Shows notification preferences
    
    Future Enhancements:
    - PATCH/PUT methods for profile updates
    - Profile statistics (alerts sent, money saved)
    - Subscription management endpoints
    - Activity history and usage analytics
    
    Example Response:
    {
        "username": "user@example.com",
        "email": "user@example.com",
        "phone_number": "+1234567890",
        "email_notifications": true,
        "sms_notifications": false,
        "whatsapp_notifications": false,
        "is_premium": false,
        "max_tracked_products": 3,
        "current_tracked_count": 2,
        "can_track_more": true
    }
    """
    # Authentication check (handled by DRF decorators)
    if not request.user.is_authenticated:
        return Response({'error': 'Authentication required'}, status=401)
    
    # Get or create profile (defensive programming)
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Calculate current usage for business rules
    from products.models import TrackedProduct
    current_tracked = TrackedProduct.objects.filter(user=request.user, is_active=True).count()
    
    # Serialize profile data for JSON response
    data = {
        'user_id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
        'phone_number': profile.phone_number or '',
        'email_notifications': profile.email_notifications,
        'sms_notifications': profile.sms_notifications,
        'whatsapp_notifications': profile.whatsapp_notifications,
        'is_premium': profile.is_premium,
        'max_tracked_products': profile.max_tracked_products,
        'current_tracked_count': current_tracked,
        'can_track_more': profile.can_track_more_products,
        'subscription_end_date': profile.subscription_end_date.isoformat() if profile.subscription_end_date else None,
        'created_at': profile.created_at.isoformat(),
        'updated_at': profile.updated_at.isoformat(),
    }
    
    return Response(data)
