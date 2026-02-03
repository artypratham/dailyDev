"""
Comprehensive logging configuration for DailyDev.
Logs are stored in /logs directory with rotation.
"""
import os
import sys
from datetime import datetime
from pathlib import Path
from loguru import logger

# Create logs directory
LOGS_DIR = Path(__file__).parent.parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Remove default logger
logger.remove()


def format_record(record):
    """Custom formatter that safely handles missing extra fields."""
    extra = record["extra"]
    user_journey = extra.get("user_journey", "-")
    user_id = extra.get("user_id", "-")
    request_id = extra.get("request_id", "-")

    format_string = (
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | "
        "{level: <8} | "
        "{name}:{function}:{line} | "
        f"journey={user_journey} | "
        f"user={user_id} | "
        f"req={request_id} | "
        "{message}\n"
    )

    if record["exception"]:
        format_string += "{exception}"

    return format_string


# Console logging format (simplified for development)
console_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)

# Add console handler
logger.add(
    sys.stdout,
    format=console_format,
    level="INFO",
    colorize=True,
)

# General application log
logger.add(
    LOGS_DIR / "app_{time:YYYY-MM-DD}.log",
    format=format_record,
    level="DEBUG",
    rotation="00:00",
    retention="30 days",
    compression="zip",
    enqueue=True,
)

# Error-specific log
logger.add(
    LOGS_DIR / "errors_{time:YYYY-MM-DD}.log",
    format=format_record,
    level="ERROR",
    rotation="00:00",
    retention="30 days",
    compression="zip",
    enqueue=True,
)

# User journey log (signup, login, article views, etc.)
logger.add(
    LOGS_DIR / "user_journey_{time:YYYY-MM-DD}.log",
    format=format_record,
    level="INFO",
    rotation="00:00",
    retention="30 days",
    compression="zip",
    enqueue=True,
    filter=lambda record: record["extra"].get("user_journey") is not None,
)


def get_logger(name: str = "dailydev"):
    """Get a logger instance with default context."""
    return logger.bind(
        user_journey=None,
        user_id=None,
        request_id=None,
    )


def get_user_journey_logger(
    journey_type: str,
    user_id: str = None,
    request_id: str = None
):
    """
    Get a logger for tracking user journeys.

    Args:
        journey_type: Type of journey (signup, login, onboarding, article_view, etc.)
        user_id: User's ID if available
        request_id: Unique request identifier
    """
    return logger.bind(
        user_journey=journey_type,
        user_id=user_id or "anonymous",
        request_id=request_id or "no-request-id",
    )


# User journey types
class JourneyType:
    SIGNUP = "signup"
    LOGIN = "login"
    LOGOUT = "logout"
    RESUME_UPLOAD = "resume_upload"
    SKILL_ANALYSIS = "skill_analysis"
    TOPIC_SELECTION = "topic_selection"
    ROADMAP_VIEW = "roadmap_view"
    ARTICLE_VIEW = "article_view"
    ARTICLE_GENERATE = "article_generate"
    ARTICLE_SAVE = "article_save"
    WHATSAPP_CONNECT = "whatsapp_connect"
    WHATSAPP_MESSAGE = "whatsapp_message"
    PROFILE_UPDATE = "profile_update"
    ERROR = "error"


# Initialize logger
app_logger = get_logger()
