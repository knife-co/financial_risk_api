import os
from .base import *

# Load development environment variables
environ.Env.read_env(os.path.join(BASE_DIR, ".env.dev"))

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Development specific settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Allow all origins for development
CORS_ALLOW_ALL_ORIGINS = True