import time

import structlog
from celery import shared_task

from src.apps.topics import models

logger = structlog.get_logger(__name__)

# TODO: Add types
# TODO: Add some more fancy return types
# TODO: Add losers queue
# TODO: Add retry mechanism
# TODO: Add beat


@shared_task
def post_message(msg_id: str, strat: str = "all") -> int:
    """Notify subs about the topic message."""
    logger.info("Message posted", id=msg_id, strategy=strat)

    if strat == "all":
        # Dispatch one-by-one, all at once
        msg = models.Message.objects.filter(uuid=msg_id).select_related("topic").first()
        if msg is None:
            logger.error("Message does not exist", id=msg_id)
            return 0

        send_all_notifications.delay(msg.topic.uuid)

        return 0

    if strat == "batch":
        # Dispatch batch-by-batch
        msg = (
            models.Message.objects.filter(uuid=msg_id)
            .select_related("topic")
            .prefetch_related("topic__subs")
            .first()
        )
        if msg is None:
            logger.error("Message does not exist", id=msg_id)
            return 0

        subs = msg.topic.subs

        batch_size = 10
        for start in range(0, subs.count(), batch_size):
            send_batch_notifications.delay(
                [
                    (sub.contact_type, sub.contact_data)
                    for sub in subs.all()[start : start + batch_size]
                ]
            )

        return 0

    if strat == "countdown":
        # Dispatch one-by-one, with a time delay
        msg = (
            models.Message.objects.filter(uuid=msg_id)
            .select_related("topic")
            .prefetch_related("topic__subs")
            .first()
        )
        if msg is None:
            logger.error("Message does not exist", id=msg_id)
            return 0

        subs = msg.topic.subs
        for i, sub in enumerate(msg.topic.subs.all()):
            send_sub_notification.apply_async(
                args=(sub.contact_type, sub.contact_data),
                countdown=i / 10,
            )

        return 0

    return 0


@shared_task
def send_all_notifications(topic_id: str) -> int:
    """Send all notifications (one by one) for given topic."""
    logger.info("Sending all notifications", topic_id=topic_id)
    topic = models.Topic.objects.filter(uuid=topic_id).first()
    if topic is None:
        logger.error("Topic does not exist", id=topic_id)
        return 0
    for sub in topic.subs.all():
        send_sub_notification.delay(sub.contact_type, sub.contact_data)
    return topic.subs.count()


@shared_task
def send_batch_notifications(subs: list[tuple[str, str]]) -> int:
    """Send batch of notifications."""
    logger.info("Sending batch notifications", subs=subs)
    for sub in subs:
        send_sub_notification.delay(*sub)
    return len(subs)


@shared_task
def send_sub_notification(contact_type: str, contact_data: str) -> int:
    """Send a single notification."""
    logger.info("Sending sub notification", type=contact_type, data=contact_data)
    time.sleep(0.1)
    logger.info("Notification sent successfully", type=contact_type, data=contact_data)
    return 1
