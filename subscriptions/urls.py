from django.urls import path
from . import views

urlpatterns = [
    # Subscription management
    path('', views.subscription_plans, name='subscription_plans'),
    path('upgrade/', views.upgrade_subscription, name='upgrade_subscription'),
    path('billing/', views.billing_history, name='billing_history'),
    
    # Stripe webhooks
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
]
