"""
WSGI config for WebServer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../WebServer")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "WebServer.settings_prod")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
