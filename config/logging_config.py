import sys
from pathlib import Path

from loguru import logger

# Get the project root path
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

# Configure Loguru
LOG_LEVEL = "DEBUG"
LOG_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

# Remove default logger
logger.remove()

# Add stdout handler with custom format
logger.add(
    sys.stderr,
    format=LOG_FORMAT,
    level=LOG_LEVEL,
    backtrace=True,
    diagnose=True,
    enqueue=True,
)

# Add file logger
log_file_path = PROJECT_ROOT / "logs" / "app.log"
logger.add(
    log_file_path,
    rotation="10 MB",  # Rotate file when it reaches 10MB
    retention="1 week",  # Keep logs for 1 week
    compression="zip",  # Compress rotated logs
    format=LOG_FORMAT,
    level=LOG_LEVEL,
    backtrace=True,
    diagnose=True,
    enqueue=True,
)

# Export logger
logger = logger
