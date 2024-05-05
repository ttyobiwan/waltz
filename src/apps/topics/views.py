from rest_framework import viewsets

from src.apps.topics import models, serializers, tasks


class TopicViewSet(viewsets.ModelViewSet):
    """Topic API viewset."""

    queryset = models.Topic.objects.all()
    serializer_class = serializers.TopicSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """Topic message API viewset."""

    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer

    def perform_create(self, serializer: serializers.MessageSerializer) -> None:
        """Create message and schedule notifications."""
        super().perform_create(serializer)
        tasks.post_message.delay(serializer.data["uuid"])


class SubViewSet(viewsets.ModelViewSet):
    """Topic subscription API viewset."""

    queryset = models.Subscription.objects.all()
    serializer_class = serializers.SubSerializer
