"""
WSGI config for deal_radar project.

This file serves as the entry point for WSGI-compatible web servers (e.g., Gunicorn, uWSGI, Heroku)
to run your Django application in production.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'deal_radar' project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deal_radar.settings')

# Get the WSGI application for use by the web server
application = get_wsgi_application()
