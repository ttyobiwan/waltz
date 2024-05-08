from rest_framework import serializers

from src.apps.topics import models


class TopicSerializer(serializers.ModelSerializer):
    """Topic serializer."""

    class Meta:
        model = models.Topic
        fields = ("uuid", "created_at", "owner", "name")
        read_only_fields = ("uuid", "created_at")


class MessageSerializer(serializers.ModelSerializer):
    """Topic message serializer."""

    class Meta:
        model = models.Message
        fields = ("uuid", "created_at", "topic", "title", "content")
        read_only_fields = ("uuid", "created_at")


class SubSerializer(serializers.ModelSerializer):
    """Topic subscription serializer."""

    class Meta:
        model = models.Subscription
        fields = ("uuid", "created_at", "topic", "contact_type", "contact_data", "confirmed")
        read_only_fields = ("uuid", "created_at", "confirmed")
