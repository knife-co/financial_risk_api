"""
WSGI config for financial_risk_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Set default to production for WSGI (since this is typically used in production)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'financial_risk_api.settings.dev')


application = get_wsgi_application()
