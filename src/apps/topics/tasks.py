import structlog
from celery import shared_task

logger = structlog.get_logger(__name__)


@shared_task
def post_message(msg_id: str) -> int:
    """Notify subs about the topic message."""
    logger.info("Message posted", id=msg_id)
    return 0
