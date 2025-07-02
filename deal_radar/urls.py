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
    
    # Frontend web interface views
    path('', include('products.urls')),        # Main user dashboard
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
