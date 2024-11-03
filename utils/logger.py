import logging
import os
from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Configure logging level and formatter
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s",
)

logger = logging.getLogger(__name__)

def info(message: str, **kwargs) -> None:
    """Logs an informational message."""
    logger.info(message, **kwargs)

def warning(message: str, **kwargs) -> None:
    """Logs a warning message."""
    logger.warning(message, **kwargs)

def error(message: str, **kwargs) -> None:
    """Logs an error message."""
    logger.error(message, **kwargs)

def debug(message: str, **kwargs) -> None:
    """Logs a debug message."""
    logger.debug(message, **kwargs)