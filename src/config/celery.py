import os

from celery import Celery

# TODO: Add redis results backend

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.settings.prod")

app = Celery("waltz")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
