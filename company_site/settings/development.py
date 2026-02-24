"""
Django development settings for company_site project.
"""

from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# For development, you can use console email backend to see emails in terminal
# Uncomment the line below if you don't want to send real emails during development
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
