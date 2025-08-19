"""
ASGI config for financial_risk_api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Set default to production for ASGI (since this is typically used in production)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'financial_risk_api.settings.dev')

application = get_asgi_application()
