"""
URL Configuration for Products App - Phase 3.1
Defines all routes for product browsing, tracking, alerts, user profile, and Stripe integration.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Home and product detail
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    # User dashboard and signup
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),

    # Product tracking
    path('product/<int:pk>/track/', views.add_to_tracking, name='add_to_tracking'),
    path('product/<int:pk>/untrack/', views.remove_from_tracking, name='remove_from_tracking'),

    # Price alert management
    path('create-alert/<int:pk>/', views.create_price_alert, name='create_price_alert'),
    path('toggle-alert/<int:pk>/', views.toggle_price_alert, name='toggle_price_alert'),
    path('delete-alert/<int:pk>/', views.delete_price_alert, name='delete_price_alert'),
    path('reset-alert/<int:pk>/', views.reset_price_alert, name='reset_price_alert'),

    # User profile and settings
    path('profile/', views.profile, name='profile'),
    path('settings/', views.user_settings, name='settings'),
    path('export/data/', views.export_data, name='export_data'),
    path('export/json/', views.export_json, name='export_json'),
    path('delete-account/', views.delete_account, name='delete_account'),

    # Category and product addition
    path('category/<slug:slug>/', views.category_products, name='category_products'),
    path('add-product/', views.add_product, name='add_product'),

    # Site support request
    path('request-site-support/', views.request_site_support, name='request_site_support'),

    # Stripe integration
    path('create-checkout-session/<str:plan_key>/', views.create_checkout_session, name='create_checkout_session'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('billing-portal/', views.create_stripe_portal_session, name='billing_portal'),
]
