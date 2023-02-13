"""
WSGI config for dj4ch14 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from mezzanine.utils.conf import real_project_name

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "%s.settings" % real_project_name("dj4ch14")
)

application = get_wsgi_application()
