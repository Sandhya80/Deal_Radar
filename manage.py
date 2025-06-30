#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

This is the main entry point for all Django management commands for the Deal Radar project.
It provides access to Django's built-in commands as well as custom management commands
for application-specific tasks.

Common Usage:
- python manage.py runserver          # Start development server
- python manage.py makemigrations     # Create database migrations
- python manage.py migrate            # Apply database migrations
- python manage.py createsuperuser    # Create admin user
- python manage.py collectstatic      # Collect static files for production
- python manage.py shell              # Open Django shell for debugging

Custom Commands (Phase 2+):
- python manage.py scrape_prices      # Run price scraping tasks
- python manage.py send_alerts        # Send pending price alerts
- python manage.py cleanup_old_data   # Clean up old price history data
- python manage.py export_user_data   # Export user data for GDPR compliance

Environment Setup:
- Automatically sets DJANGO_SETTINGS_MODULE to 'deal_radar.settings'
- Requires virtual environment activation for proper dependency management
- Loads environment variables from .env file through Django settings

Error Handling:
- Provides clear error messages for common setup issues
- Checks for Django installation and virtual environment
- Guides users through proper environment configuration
"""

import os
import sys


def main():
    """
    Run administrative tasks.
    
    This function sets up the Django environment and executes the requested
    management command with proper error handling and environment validation.
    
    Process:
    1. Set default Django settings module
    2. Import Django's command-line execution function
    3. Execute the requested command with provided arguments
    4. Handle common setup errors with helpful messages
    
    Error Cases:
    - Django not installed or not in PYTHONPATH
    - Virtual environment not activated
    - Missing or incorrect settings configuration
    - Database connection issues
    """
    # Set default settings module for Deal Radar project
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deal_radar.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Execute the requested Django management command
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
