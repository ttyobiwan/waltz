import enum
import random
import time

import structlog
from celery import Task, shared_task
from django.db.models import Count

from src.apps.topics import models

logger = structlog.get_logger(__name__)

# TODO: Add beat
# TODO: Add cache


def move_to_losers_queue(
    self: Task,
    exc: Exception,
    task_id: str,
    args: tuple,
    kwargs: dict,
    einfo: str,
):
    """Send task to the losers queue with extra countdown."""
    del exc, task_id, einfo
    logger.info("Sending to losers queue", args=args, kwargs=kwargs)
    if kwargs.get("countdown") is None:
        kwargs["countdown"] = 10
    else:
        kwargs["countdown"] += kwargs["countdown"]
    self.apply_async(args, kwargs, queue="losers", countdown=kwargs["countdown"])


class DispatchStrategy(str, enum.Enum):
    """Notification dispatch strategy."""

    ALL = "all"
    BATCH = "batch"
    CD = "countdown"


@shared_task
def post_message(msg_id: str, strat: DispatchStrategy = DispatchStrategy.ALL) -> int:
    """Notify subs about the topic message."""
    logger.info("Message posted", id=msg_id, strategy=strat)

    match strat:
        case DispatchStrategy.ALL:
            # Dispatch one-by-one, all at once
            msg = (
                models.Message.objects.filter(uuid=msg_id)
                .select_related("topic")
                .annotate(subs_count=Count("topic__subs"))
                .first()
            )
            if msg is None:
                logger.error("Message does not exist", id=msg_id)
                return 0
            send_all_notifications.delay(msg.topic.uuid)
            return msg.subs_count

        case DispatchStrategy.BATCH:
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

            return subs.count()

        case DispatchStrategy.CD:
            # Dispatch one-by-one, with a time delay for each
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

            return subs.count()

        case _:
            logger.error("Invalid dispatch strategy", strategy=strat)
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


@shared_task(
    autoretry_for=(Exception,),
    max_retries=1,
    retry_backoff=True,
    on_failure=move_to_losers_queue,
)
def send_sub_notification(contact_type: str, contact_data: str, **kwargs) -> int:
    """Send a single notification."""
    logger.info("Sending sub notification", type=contact_type, data=contact_data, kwargs=kwargs)

    fail = random.randint(0, 1)  # noqa:S311
    if fail:
        raise ConnectionError("Task got unlucky")

    time.sleep(0.1)
    logger.info("Notification sent successfully", type=contact_type, data=contact_data)
    return 1
