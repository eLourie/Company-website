"""
Django production settings for company_site project.
Configured for TimeWeb hosting.
"""

from pathlib import Path
from .base import *

# Ensure os module is available after wildcard import
import os

DEBUG = False

# Get allowed hosts from environment variable (comma-separated)
ALLOWED_HOSTS = [h.strip() for h in os.getenv('ALLOWED_HOSTS', '').split(',') if h.strip()]

# =============================================================================
# TIMEWEB HOSTING CONFIGURATION
# =============================================================================
# On TimeWeb, the project is located in ~/public_html/
# Structure:
#   ~/public_html/          <- Django project (BASE_DIR)
#   ~/venv/                 <- Virtual environment
#   ~/public_html/static/   <- Collected static files
#   ~/public_html/media/    <- Media files

# Check if running on TimeWeb (via environment variable)
TIMEWEB_MODE = os.getenv('TIMEWEB_MODE', 'False').lower() == 'true'

if TIMEWEB_MODE:
    # On TimeWeb, BASE_DIR is ~/public_html/
    BASE_DIR = Path(os.path.expanduser('~/public_html'))

    # Static and media files paths for TimeWeb
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'static'
    STATICFILES_DIRS = []  # No additional static dirs on TimeWeb

    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'

    # Templates path
    TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']

    # Locale path
    LOCALE_PATHS = [BASE_DIR / 'locale']

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================
# MySQL for production on TimeWeb
DB_ENGINE = os.getenv('DB_ENGINE', 'mysql')

if DB_ENGINE == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME', ''),
            'USER': os.getenv('DB_USER', ''),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        }
    }
else:
    # Fallback to SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# =============================================================================
# SECURITY SETTINGS
# =============================================================================
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS settings (enable after confirming HTTPS works)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# HTTPS settings for TimeWeb (enable if using SSL)
if os.getenv('USE_HTTPS', 'False').lower() == 'true':
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# =============================================================================
# STATIC FILES
# =============================================================================
# Use simpler storage for TimeWeb compatibility
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
