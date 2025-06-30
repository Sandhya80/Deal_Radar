"""
Django settings for Deal Radar project.

This file contains all configuration settings for the Deal Radar application.
Settings are organized by functionality and use environment variables for
deployment flexibility across development, staging, and production environments.

Architecture Philosophy:
- Environment-based configuration (12-factor app methodology)
- Modular app organization for maintainability
- Security-first approach with production overrides
- Optimized for both development speed and production reliability

For more information on Django settings:
https://docs.djangoproject.com/en/4.2/topics/settings/
"""

import os
from pathlib import Path
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# This is the absolute path to the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment variables configuration using django-environ
# This allows us to use .env files and environment variables
env = environ.Env(
    DEBUG=(bool, False)  # Default to False for security
)

# Take environment variables from .env file if it exists
# This enables local development with sensitive data kept out of version control
environ.Env.read_env(BASE_DIR / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY is used for cryptographic signing throughout Django
# In production, this should be a long, random, unique string
SECRET_KEY = env('SECRET_KEY', default='django-insecure-change-me-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG mode shows detailed error pages and serves static files
# Always set to False in production for security
DEBUG = env('DEBUG', default=True)

# ALLOWED_HOSTS controls which domains can serve this Django application
# Required when DEBUG=False to prevent HTTP Host header attacks
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Application definition
# Organized into categories for better maintainability

# Django Core Apps - Essential Django functionality
DJANGO_APPS = [
    'django.contrib.admin',          # Admin interface for data management
    'django.contrib.auth',           # User authentication system
    'django.contrib.contenttypes',   # Content type framework
    'django.contrib.sessions',       # Session framework for user state
    'django.contrib.messages',       # Messaging framework for notifications
    'django.contrib.staticfiles',    # Static file management
]

# Third Party Apps - External packages that extend Django
THIRD_PARTY_APPS = [
    'rest_framework',                # RESTful API framework
    'rest_framework.authtoken',      # Token-based authentication for API
    'corsheaders',                   # Cross-Origin Resource Sharing for frontend
    'django_bootstrap5',             # Bootstrap integration for UI
    'allauth',                       # Advanced authentication (email login)
    'allauth.account',               # Account management
    'allauth.socialaccount',         # Social media login (future enhancement)
    'django_celery_beat',            # Periodic task scheduling
]

# Local Apps - Our custom Deal Radar functionality
LOCAL_APPS = [
    'users',           # User profiles and authentication extensions
    'products',        # Product tracking and price history
    'notifications',   # Email/SMS/WhatsApp alert system
    'subscriptions',   # Stripe payment and subscription management
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Django Middleware Configuration
# Middleware processes requests and responses in order
# Each piece handles a specific aspect of request processing
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',                    # CORS headers for API access
    'django.middleware.security.SecurityMiddleware',           # Security headers
    'whitenoise.middleware.WhiteNoiseMiddleware',              # Static file serving (Heroku)
    'django.contrib.sessions.middleware.SessionMiddleware',    # Session management
    'django.middleware.common.CommonMiddleware',               # Common functionality
    'django.middleware.csrf.CsrfViewMiddleware',               # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware', # User authentication
    'allauth.account.middleware.AccountMiddleware',            # Django AllAuth integration
    'django.contrib.messages.middleware.MessageMiddleware',    # Flash messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
]

# URL Configuration
# Root URL configuration file that includes all app URLs
ROOT_URLCONF = 'deal_radar.urls'

# Template Configuration
# Django's template engine configuration for rendering HTML
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Global template directory
        'APP_DIRS': True,                  # Look for templates in each app's templates/ dir
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',    # Debug info in templates
                'django.template.context_processors.request',  # Request object in templates
                'django.contrib.auth.context_processors.auth', # User info in templates
                'django.contrib.messages.context_processors.messages', # Flash messages
            ],
        },
    },
]

# WSGI Application
# Entry point for WSGI-compatible web servers
WSGI_APPLICATION = 'deal_radar.wsgi.application'

# Database Configuration
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Development Database: SQLite (simple, no setup required)
# Fast for development, supports all Django features
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Production Database: PostgreSQL (when DATABASE_URL is provided)
# Heroku and most production environments use PostgreSQL
# Automatically switches when DATABASE_URL environment variable is set
DATABASE_URL = env('DATABASE_URL', default=None)
if DATABASE_URL:
    import dj_database_url
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL)

# Password Validation
# Django's built-in password validation for user security
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        # Prevent passwords too similar to user information
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # Enforce minimum password length (default: 8 characters)
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        # Prevent common passwords (e.g., "password123")
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # Prevent purely numeric passwords
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# Language and timezone settings
LANGUAGE_CODE = 'en-us'  # Default language
TIME_ZONE = 'UTC'        # Use UTC for consistency across timezones
USE_I18N = True          # Enable internationalization
USE_TZ = True            # Enable timezone support (important for global users)

# Static Files Configuration (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# URL prefix for static files served by Django
STATIC_URL = '/static/'

# Directory where collectstatic collects all static files for production
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Additional directories to search for static files during development
STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Global static files directory
]

# Media Files Configuration (user-uploaded files)
# URL prefix for media files (product images, user avatars)
MEDIA_URL = '/media/'

# Directory where uploaded files are stored
MEDIA_ROOT = BASE_DIR / 'media'

# Default Primary Key Field Type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
# Use BigAutoField for better performance with large datasets
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework Configuration
# Settings for API functionality and mobile app support
REST_FRAMEWORK = {
    # Authentication methods for API endpoints
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',    # Token-based auth for mobile
        'rest_framework.authentication.SessionAuthentication',  # Session auth for web
    ],
    # Default permission requirements
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Require authentication by default
    ],
    # Pagination settings for large datasets
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,  # Products per page
}

# Celery Configuration (Background Task Processing)
# Used for web scraping, sending notifications, and scheduled tasks
CELERY_BROKER_URL = env('REDIS_URL', default='redis://localhost:6379/0')      # Message broker
CELERY_RESULT_BACKEND = env('REDIS_URL', default='redis://localhost:6379/0')   # Result storage
CELERY_ACCEPT_CONTENT = ['json']        # Only accept JSON serialized content
CELERY_TASK_SERIALIZER = 'json'         # Serialize task data as JSON
CELERY_RESULT_SERIALIZER = 'json'       # Serialize result data as JSON
CELERY_TIMEZONE = TIME_ZONE             # Use same timezone as Django

# Email Configuration (Phase 3: Notifications)
# Email backend and SMTP settings for sending price alerts
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = env('EMAIL_HOST', default='')
EMAIL_PORT = env('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = env('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='Deal Radar <noreply@dealradar.com>')

# Twilio Configuration (Phase 3: SMS/WhatsApp Notifications)
# Credentials for sending SMS and WhatsApp price alerts
TWILIO_ACCOUNT_SID = env('TWILIO_ACCOUNT_SID', default='')
TWILIO_AUTH_TOKEN = env('TWILIO_AUTH_TOKEN', default='')
TWILIO_PHONE_NUMBER = env('TWILIO_PHONE_NUMBER', default='')

# Stripe Configuration (Phase 4: Subscription Payments)
# Payment processing for premium subscriptions
STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY', default='')
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY', default='')
STRIPE_WEBHOOK_SECRET = env('STRIPE_WEBHOOK_SECRET', default='')

# Cloudinary Configuration (Optional: Image Storage)
# Cloud storage for product screenshots and user images
CLOUDINARY_CLOUD_NAME = env('CLOUDINARY_CLOUD_NAME', default='')
CLOUDINARY_API_KEY = env('CLOUDINARY_API_KEY', default='')
CLOUDINARY_API_SECRET = env('CLOUDINARY_API_SECRET', default='')

# Security Settings (Production Environment)
# These settings are automatically applied when DEBUG=False
if not DEBUG:
    SECURE_SSL_REDIRECT = True              # Force HTTPS
    SECURE_HSTS_SECONDS = 31536000          # HSTS header (1 year)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True   # HSTS for subdomains
    SECURE_HSTS_PRELOAD = True              # HSTS preload directive
    SECURE_CONTENT_TYPE_NOSNIFF = True      # Prevent MIME sniffing
    SECURE_BROWSER_XSS_FILTER = True       # XSS protection
    SESSION_COOKIE_SECURE = True           # Secure session cookies
    CSRF_COOKIE_SECURE = True              # Secure CSRF cookies

# CORS Settings (Cross-Origin Resource Sharing)
# Allow frontend applications to access our API
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",    # React development server
    "http://127.0.0.1:3000",    # Alternative React dev server
]

# Django AllAuth Configuration
# Settings for advanced authentication features (Updated for latest version)
ACCOUNT_EMAIL_VERIFICATION = 'optional'    # Email verification not required
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True # Auto-login after email confirmation
ACCOUNT_LOGOUT_REDIRECT_URL = '/'          # Redirect after logout
ACCOUNT_LOGIN_REDIRECT_URL = '/dashboard/' # Redirect after login

# Modern AllAuth configuration (replaces deprecated settings)
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*']  # Required signup fields
ACCOUNT_LOGIN_METHODS = {'email'}          # Login with email only

# Logging Configuration
# Console logging for development, file logging for production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'deal_radar': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
