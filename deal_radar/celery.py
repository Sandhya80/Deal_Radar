"""
Celery Configuration for Deal Radar

This module configures Celery for background task processing in the Deal Radar application.
Celery enables asynchronous processing of time-intensive tasks like web scraping,
email notifications, and scheduled price monitoring.

Key Functionality:
- Web scraping tasks for price updates
- Email/SMS notification delivery
- Scheduled price monitoring jobs
- Database cleanup and maintenance tasks
- Report generation and analytics

Task Categories:
1. Scraping Tasks: Product price fetching from e-commerce sites
2. Notification Tasks: Email, SMS, and WhatsApp delivery
3. Monitoring Tasks: Price change detection and alert generation
4. Maintenance Tasks: Data cleanup and system health checks
5. Analytics Tasks: Usage statistics and reporting

Redis Integration:
- Message broker for task queue management
- Result backend for task status and return values
- Supports high-throughput task processing
- Provides reliability and persistence for critical tasks

Deployment Considerations:
- Requires Redis server for production
- Worker processes scale horizontally
- Beat scheduler for periodic tasks
- Monitoring and alerting for task failures
"""

import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
# This ensures Celery uses the same configuration as the Django application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'deal_radar.settings')

# Create Celery application instance
# Name should match the Django project name for consistency
app = Celery('deal_radar')

# Configure Celery using Django settings
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# The 'CELERY' namespace separates Celery settings from other Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover task modules from all registered Django apps
# This looks for 'tasks.py' files in each Django app and imports task functions
app.autodiscover_tasks()

# Task Routing Configuration (Phase 2+)
# Route different types of tasks to specific queues for better resource management
# app.conf.task_routes = {
#     'products.tasks.scrape_product_price': {'queue': 'scraping'},
#     'notifications.tasks.send_email_alert': {'queue': 'notifications'},
#     'notifications.tasks.send_sms_alert': {'queue': 'notifications'},
#     'analytics.tasks.generate_report': {'queue': 'analytics'},
# }

# Task Configuration
app.conf.update(
    # Task execution settings
    task_serializer='json',           # Use JSON for task serialization
    accept_content=['json'],          # Only accept JSON content
    result_serializer='json',         # Serialize results as JSON
    timezone='UTC',                   # Use UTC timezone for consistency
    enable_utc=True,                  # Enable UTC timezone handling
    
    # Task routing and retry settings
    task_default_retry_delay=60,      # Retry failed tasks after 60 seconds
    task_max_retries=3,               # Maximum retry attempts
    task_acks_late=True,              # Acknowledge tasks after completion
    worker_prefetch_multiplier=1,     # Process one task at a time for accuracy
    
    # Result backend settings
    result_expires=3600,              # Results expire after 1 hour
    result_persistent=True,           # Persist results in Redis
    
    # Beat scheduler settings (for periodic tasks)
    beat_schedule={
        # Example scheduled tasks for Phase 2+
        # 'scrape-all-products': {
        #     'task': 'products.tasks.scrape_all_products',
        #     'schedule': crontab(minute=0, hour='*/2'),  # Every 2 hours
        # },
        # 'send-daily-digest': {
        #     'task': 'notifications.tasks.send_daily_digest',
        #     'schedule': crontab(hour=9, minute=0),  # Daily at 9 AM
        # },
        # 'cleanup-old-data': {
        #     'task': 'maintenance.tasks.cleanup_old_price_history',
        #     'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
        # },
    },
)

@app.task(bind=True)
def debug_task(self):
    """
    Debug task for testing Celery functionality
    
    This task is used for testing and debugging the Celery setup.
    It prints the task request information and can be used to verify
    that workers are running correctly and can process tasks.
    
    Usage:
    - Call from Django shell: debug_task.delay()
    - Monitor worker logs for output
    - Verify task completion in Redis/result backend
    
    Args:
        self: Task instance (automatically provided by bind=True)
    
    Returns:
        str: Debug information about the task request
    """
    print(f'Request: {self.request!r}')
    return f'Debug task executed successfully. Request ID: {self.request.id}'


# Example task definitions for future phases:

# @app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
# def scrape_product_price(self, product_id):
#     """Scrape current price for a specific product"""
#     pass

# @app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 2})
# def send_price_alert(self, user_id, product_id, old_price, new_price):
#     """Send price drop alert to user via their preferred channels"""
#     pass

# @app.task
# def generate_daily_report():
#     """Generate daily analytics report for admin dashboard"""
#     pass
