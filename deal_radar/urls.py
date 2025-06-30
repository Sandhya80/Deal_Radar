"""
URL configuration for deal_radar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/

Architecture Logic:
- Separates frontend views from API endpoints
- Uses Django's include() for modular URL organization
- Follows RESTful conventions for API structure
- Supports both web interface and API access
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin interface for data management and debugging
    path('admin/', admin.site.urls),
    
    # Authentication system (django-allauth)
    # Provides: /accounts/login/, /accounts/logout/, /accounts/signup/
    path('accounts/', include('allauth.urls')),
    
    # API endpoints for mobile apps or frontend frameworks
    path('api/auth/', include('users.urls')),           # User management API
    path('api/products/', include('products.urls')),     # Product tracking API
    path('api/notifications/', include('notifications.urls')),  # Notification API
    path('api/subscriptions/', include('subscriptions.urls')),  # Payment API
    
    # Frontend web interface views
    path('', include('users.urls')),                     # Home page and auth views
    path('dashboard/', include('products.urls')),        # Main user dashboard
    path('subscriptions/', include('subscriptions.urls')),  # Subscription management
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
