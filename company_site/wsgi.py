"""
WSGI config for company_site project.
"""

import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

# Load environment variables from .env file
load_dotenv()

# Get environment from .env (default to production for WSGI)
env = os.getenv('DJANGO_ENV', 'production')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'company_site.settings.{env}')

application = get_wsgi_application()
