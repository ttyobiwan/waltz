import pytest
from rest_framework.test import APIClient


@pytest.fixture
def http_client() -> APIClient:
    """Return an API client for test purposes."""
    return APIClient()


@pytest.fixture(autouse=True)
def django_settings(settings):
    """Return overwritten Django settings."""
    settings.CELERY_TASK_ALWAYS_EAGER = True
    return settings
