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
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin interface for data management and debugging
    path('admin/', admin.site.urls),

    # Frontend web interface views (includes home, dashboard, signup, etc.)
    path('', include('products.urls')),

    # Authentication URLs for login/logout (Phase 3)
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # API endpoints can be added here in future phases
    # path('api/', include('api.urls')),
]

# Serve static and media files during development only
# In production, these are served by the web server (e.g., Heroku, WhiteNoise)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
