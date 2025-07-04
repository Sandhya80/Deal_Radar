"""
URL Configuration for Products App - Phase 3.1
User authentication and personal tracking
"""

from django.urls import path
from . import views

urlpatterns = [
    # Phase 2.5 URLs (existing)
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    
    # Phase 3 URLs (new)
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('product/<int:pk>/track/', views.add_to_tracking, name='add_to_tracking'),
    path('product/<int:pk>/untrack/', views.remove_from_tracking, name='remove_from_tracking'),

    # Price Alert URLs
    path('create-alert/<int:pk>/', views.create_price_alert, name='create_price_alert'),
    path('toggle-alert/<int:pk>/', views.toggle_price_alert, name='toggle_price_alert'),
    path('delete-alert/<int:pk>/', views.delete_price_alert, name='delete_price_alert'),
    path('reset-alert/<int:pk>/', views.reset_price_alert, name='reset_price_alert'),
]
