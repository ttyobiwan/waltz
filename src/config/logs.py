import logging
import time
from typing import Callable

import structlog
from django.http import HttpRequest, HttpResponse
from structlog.types import EventDict

access_logger = structlog.stdlib.get_logger("hahahandler")


def rename_event_key(_, __, event_dict: EventDict) -> EventDict:
    """Rename event key in the log.

    Log entries keep the text message in the `event` field, but Datadog
    uses the `message` field. This processor moves the value from one field to
    the other.
    """
    event_dict["message"] = event_dict.pop("event")
    return event_dict


def drop_color_message_key(_, __, event_dict: EventDict) -> EventDict:
    """Drop color key from the log.

    Uvicorn logs the message a second time in the extra `color_message`, but we don't
    need it. This processor drops the key from the event dict if it exists.
    """
    event_dict.pop("color_message", None)
    return event_dict


def setup_logging(enable_json: bool = False, log_level: str = "INFO"):
    """Set up structlog logging."""
    timestamper = structlog.processors.TimeStamper(fmt="iso")

    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.stdlib.ExtraAdder(),
        drop_color_message_key,
        timestamper,
        structlog.processors.StackInfoRenderer(),
    ]

    if enable_json:
        # Rename the `event` key to `message` only in JSON logs, as Datadog looks for
        # the `message` key but the pretty ConsoleRenderer looks for `event`
        shared_processors.append(rename_event_key)
        # Format the exception only for JSON logs, as we want to pretty-print them when
        # using the ConsoleRenderer
        shared_processors.append(structlog.processors.format_exc_info)

    structlog.configure(
        processors=shared_processors
        + [
            # Prepare event dict for `ProcessorFormatter`.
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    log_renderer: structlog.types.Processor
    if enable_json:
        log_renderer = structlog.processors.JSONRenderer()
    else:
        log_renderer = structlog.dev.ConsoleRenderer()

    formatter = structlog.stdlib.ProcessorFormatter(
        # These run ONLY on `logging` entries that do NOT originate within structlog.
        foreign_pre_chain=shared_processors,
        # These run on ALL entries after the pre_chain is done.
        processors=[
            # Remove _record & _from_structlog.
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            log_renderer,
        ],
    )

    handler = logging.StreamHandler()
    # Use `ProcessorFormatter` to format all `logging` entries.
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level.upper())


class LoggingMiddleware:
    """Structured logging middleware."""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Log info about the request."""
        structlog.contextvars.clear_contextvars()

        start_time = time.perf_counter_ns()

        # TODO: Add try here
        response = self.get_response(request)

        process_time = time.perf_counter_ns() - start_time

        status_code = response.status_code
        url = request.build_absolute_uri()
        path = request.path
        client_host = request.get_host()
        client_port = request.get_port()
        http_method = request.method
        http_version = request.META.get("SERVER_PROTOCOL", None)
        if http_version is None:
            http_version = f"HTTP/{request.scope.get('http_version')}"  # type: ignore
        # Recreate the Uvicorn access log format,
        # but add all parameters as structured information.
        access_logger.info(
            f"""{client_host} - "{http_method} {path} {http_version}" {status_code}""",
            http={
                "url": url,
                "path": path,
                "status_code": status_code,
                "method": http_method,
                "version": http_version,
            },
            network={"client": {"ip": client_host, "port": client_port}},
            duration=process_time,
        )

        return response
