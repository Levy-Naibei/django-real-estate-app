from __future__ import absolute_import
import os

from celery import Celery

from real_estate.settings import base

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "real_estate.settings.development")

# celery app instance
app = Celery("real_estate")

# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("real_estate.settings.development", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: base.INSTALLED_APPS)
