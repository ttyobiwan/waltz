import uuid

from django.db import models

from src.apps.topics import types


class Topic(models.Model):
    """Topic model."""

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.CharField(max_length=127)
    name = models.CharField(max_length=127)

    def __str__(self) -> str:
        return f"{self.name} by {self.owner}"


class Message(models.Model):
    """Topic message model."""

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="messages")
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self) -> str:
        return f"Message for {self.topic.name}"


class Subscription(models.Model):
    """Subscription model."""

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="subs")
    contact_type = models.CharField(max_length=31, choices=types.ContactType.choices())
    contact_data = models.TextField(null=False, blank=False)
    confirmed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.contact_type.lower().capitalize()} sub for {self.topic.name}"
