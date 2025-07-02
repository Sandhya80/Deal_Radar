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
]
