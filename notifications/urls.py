from django.urls import path
from . import views

urlpatterns = [
    # Notification settings
    path('settings/', views.notification_settings, name='notification_settings'),
    
    # API endpoints for notifications
    path('api/test/', views.test_notification, name='test_notification'),
]
