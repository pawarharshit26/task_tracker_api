import logging
import structlog
import sys
from app.core.config import settings


def setup_logging():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")

    if settings.ENV == "local":
        renderer = structlog.dev.ConsoleRenderer(colors=True)
    else:
        renderer = structlog.processors.JSONRenderer()

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            renderer,  # 👈 JSON logs
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def get_logger(name: str = None):
    """
    Returns a structlog logger bound with module name.
    Usage: logger = get_logger(__name__)
    """
    logger = structlog.get_logger()
    if name:
        logger = logger.bind(module=name)
    return logger
