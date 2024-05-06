import os

from celery import Celery, signals

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.config.settings.prod")

app = Celery("waltz")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@signals.setup_logging.connect
def on_celery_setup_logging(**_) -> None:
    """Disable Celery logging config by config from logs.py."""
