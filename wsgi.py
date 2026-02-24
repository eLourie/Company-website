"""
WSGI entry point for TimeWeb hosting.
This file should be placed in ~/public_html/index.wsgi (or wsgi.py)
"""

import os
import sys

# =============================================================================
# VIRTUAL ENVIRONMENT ACTIVATION
# =============================================================================
# Activate the virtual environment
# On TimeWeb, venv is usually in ~/venv/ (outside public_html)
venv_path = os.path.expanduser('~/public_html/venv')
activate_this = os.path.join(venv_path, 'bin', 'activate_this.py')

if os.path.exists(activate_this):
    exec(open(activate_this).read(), {'__file__': activate_this})

# =============================================================================
# PATH CONFIGURATION
# =============================================================================
# Add the project directory to Python path
project_path = os.path.expanduser('~/public_html')
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# =============================================================================
# ENVIRONMENT VARIABLES
# =============================================================================
# Load .env file
from dotenv import load_dotenv
env_file = os.path.join(project_path, '.env')
if os.path.exists(env_file):
    load_dotenv(env_file)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'company_site.settings.production')

# =============================================================================
# DJANGO APPLICATION
# =============================================================================
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()