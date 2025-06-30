"""
URL Configuration for Products App

This module defines URL patterns for product tracking functionality.
It includes both web interface routes and API endpoints for mobile/frontend access.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# API Router for REST endpoints
router = DefaultRouter()

# URL patterns
urlpatterns = [
    # Frontend views
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    
    # API endpoints
    path('api/', include(router.urls)),
    path('api/list/', views.product_list_api, name='product_list_api'),
]
