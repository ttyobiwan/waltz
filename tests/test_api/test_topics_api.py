from unittest import mock
import pytest

from django.urls import reverse
from rest_framework import status

from src.apps.topics import types

pytestmark = pytest.mark.django_db


class TestTopicAPI:
    """Test cases for the topics API."""

    def test_create_message(self, http_client):
        """Test posting a new message to the topic."""
        # Create topic
        url = reverse("api:v1:topics:topics-list")
        response = http_client.post(url, data={"owner": "Conor McGregor", "name": "Test Topic"})
        assert response.status_code == status.HTTP_201_CREATED
        topic_id = response.data["uuid"]

        # Add some subs
        calls = []
        url = reverse("api:v1:topics:subs-list")
        for i in range(5):
            response = http_client.post(
                url,
                data={
                    "topic": topic_id,
                    "contact_type": types.ContactType.DISCORD.value,
                    "contact_data": str(i),
                },
            )
            assert response.status_code == status.HTTP_201_CREATED
            calls.append(mock.call(types.ContactType.DISCORD.value, str(i)))

        # Add message
        url = reverse("api:v1:topics:messages-list")
        with mock.patch("src.apps.topics.tasks.send_sub_notification.delay") as mock_send:
            response = http_client.post(
                url,
                data={"topic": topic_id, "title": "Test Message", "content": "Test content"},
            )
        assert response.status_code == status.HTTP_201_CREATED

        mock_send.assert_has_calls(calls, any_order=True)
