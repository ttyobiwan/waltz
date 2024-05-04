from rest_framework import viewsets

from src.apps.topics import models, serializers


class TopicViewSet(viewsets.ModelViewSet):
    """Topic API viewset."""

    queryset = models.Topic.objects.all()
    serializer_class = serializers.TopicSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """Topic message API viewset."""

    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer


class SubViewSet(viewsets.ModelViewSet):
    """Topic subscription API viewset."""

    queryset = models.Subscription.objects.all()
    serializer_class = serializers.SubSerializer
