import random

import structlog
from django.core.management.base import BaseCommand, CommandParser

from src.apps.topics import models, types

logger = structlog.get_logger(__name__)


class Command(BaseCommand):
    """Command for creating a topic with high amount of subs."""

    help = "Create a topic with high amount of subs"

    def add_arguments(self, parser: CommandParser) -> None:
        """Add command arguments."""
        parser.add_argument(
            "--owner",
            help="Specifies the topic owner",
        )
        parser.add_argument(
            "--name",
            help="Specifies the topic name",
        )
        parser.add_argument(
            "--subs",
            help="Specifies the number of subs",
        )

    def handle(self, *_, **options):
        """Generate subs."""
        owner = options["owner"] or str(random.randint(1, 10000))  # noqa:S311
        name = options["name"] or str(random.randint(1, 10000))  # noqa:S311
        sub_no = int(options["subs"]) or 100
        logger.info("Creating hot topic", owner=owner, name=name, subs=sub_no)

        topic, _ = models.Topic.objects.get_or_create(owner=owner, name=name)

        subs = [
            models.Subscription(
                topic=topic,
                contact_type=list(types.ContactType)[
                    random.randint(0, len(types.ContactType) - 1)  # noqa:S311
                ].value,
                contact_data=str(random.randint(1, 10000)),  # noqa:S311
                confirmed=True,
            )
            for _ in range(sub_no)
        ]
        models.Subscription.objects.bulk_create(subs)

        logger.info("Bulk creation completed")
