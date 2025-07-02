"""
URL Configuration for Products App - Phase 2
Simple product tracking functionality
"""

from django.urls import path
from . import views

urlpatterns = [
    # Phase 2 - Basic functionality only
    path('', views.home, name='home'),
    # Phase 3+ URLs will be added later
]
