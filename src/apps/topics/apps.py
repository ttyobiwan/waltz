from django.apps import AppConfig


class TopicsConfig(AppConfig):
    """Topics app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "src.apps.topics"
    label = "topics"
