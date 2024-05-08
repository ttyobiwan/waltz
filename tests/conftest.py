from typing import Any
import pytest
from rest_framework.test import APIClient


@pytest.fixture
def http_client() -> APIClient:
    """Return an API client for test purposes."""
    return APIClient()


@pytest.fixture(autouse=True)
def django_settings[T: Any](settings: T) -> T:  # Couldn't stop myself
    settings.CELERY_TASK_ALWAYS_EAGER = True
    return settings
