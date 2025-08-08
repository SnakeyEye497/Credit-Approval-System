"""
ASGI config for credit_approval project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

# This application is used to run the Django project with ASGI support.
# It allows for handling asynchronous requests and WebSocket connections.
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credit_approval.settings')

application = get_asgi_application()
