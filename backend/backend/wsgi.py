"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application


sys.path.append('../../../Plinic-Backend')
sys.path.append('venv/lib/python3.10/site-packages')
sys.path.append('../../backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.backend.settings.dev')

application = get_wsgi_application()
