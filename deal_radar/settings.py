# -----------------------------------------------
# Deal Radar Django Settings
# -----------------------------------------------
# This file contains all configuration for the Deal Radar app,
# including security, database, authentication, email, Stripe,
# Celery, logging, and third-party integrations.
# -----------------------------------------------

import environ
import os
from decouple import config
from dotenv import load_dotenv
from pathlib import Path
import dj_database_url

# Load environment variables from .env file for secrets and configs
load_dotenv()  # This will read your .env file

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# -------------------------------
# Security Settings
# -------------------------------
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-in-production')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,.herokuapp.com,my-dealradar-app-61098a40edc6.herokuapp.com', cast=lambda v: [s.strip() for s in v.split(',')])

# Site domain for building absolute URLs (used in emails, etc.)
SITE_DOMAIN = "https://my-dealradar-app-61098a40edc6.herokuapp.com"

# -------------------------------
# Application Definition
# -------------------------------
INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Custom apps
    'products',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Add WhiteNoise for static file serving in production
if not DEBUG:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

ROOT_URLCONF = 'deal_radar.urls'

# -------------------------------
# Templates Configuration
# -------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Custom context processor for product categories
                'products.context_processors.product_category_choices',
            ],
        },
    },
]

WSGI_APPLICATION = 'deal_radar.wsgi.application'

# -------------------------------
# Database Configuration
# -------------------------------
# Uses DATABASE_URL from .env for cloud deployment (Heroku, etc.)
DATABASES = {
    'default': env.db(),  # This uses DATABASE_URL from .env
}

# -------------------------------
# Password Validation
# -------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# -------------------------------
# Internationalization
# -------------------------------
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_TZ = True

# -------------------------------
# Static and Media Files
# -------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Use WhiteNoise for static files in production
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# -------------------------------
# Default Primary Key Field Type
# -------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------------
# Authentication URLs
# -------------------------------
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'

# -------------------------------
# Email Configuration
# -------------------------------
# Used for sending notifications and alerts
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='Deal Radar <noreply@dealradar.com>')

# -------------------------------
# Twilio Configuration (SMS/WhatsApp)
# -------------------------------
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = config('TWILIO_WHATSAPP_NUMBER')

# -------------------------------
# Cache Configuration
# -------------------------------
# Used for session and price tracking caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}

# -------------------------------
# Session Configuration
# -------------------------------
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_SAVE_EVERY_REQUEST = True

# -------------------------------
# Logging Configuration
# -------------------------------
# Logs to file in development, to console on Heroku
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'] if not DEBUG else ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'products': {
            'handlers': ['console', 'file'] if not DEBUG else ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# -------------------------------
# Security Settings
# -------------------------------
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# -------------------------------
# Development vs Production Settings
# -------------------------------
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    SECURE_SSL_REDIRECT = False
else:
    # Production settings
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Heroku-specific logging configuration
if os.environ.get('DYNO'):  # True on Heroku
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }
# else: keep the file-based logging for local development

# -------------------------------
# Cloudinary Storage for Media Files
# -------------------------------
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# -------------------------------
# Stripe Payment Integration
# -------------------------------
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')

# Stripe subscription plans and feature limits
STRIPE_PLANS = {
    "free": {
        "name": "Free",
        "price_id": None,  # No Stripe price for free
        "price": 0,
        "product_limit": 3,
        "channels": ["email"],
    },
    "basic": {
        "name": "Basic",
        "price_id": "price_1Rl75p2eZ8a3DqWzLnBz5BmS",  # From Stripe
        "price": 2.99,
        "product_limit": 10,
        "channels": ["email", "sms"],
    },
    "premium": {
        "name": "Premium",
        "price_id": "price_1Rl76G2eZ8a3DqWzyK9xEcLH",  # From Stripe
        "price": 4.99,
        "product_limit": None,  # Unlimited
        "channels": ["email", "sms", "whatsapp"],
    },
}

# End of settings.py