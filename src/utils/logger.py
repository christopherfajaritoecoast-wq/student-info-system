"""Logging setup for the application."""

import logging
from pathlib import Path

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOGGER_NAME = "student_info_system"


def setup_logger(log_file, level=logging.DEBUG):
    """Create (or reuse) the application logger writing to ``log_file``."""
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(level)
    logger.propagate = False

    if not logger.handlers:  # avoid duplicate handlers on repeated calls
        formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
        try:
            Path(log_file).parent.mkdir(parents=True, exist_ok=True)
            handler = logging.FileHandler(log_file, encoding="utf-8")
        except (OSError, PermissionError):
            handler = logging.NullHandler()  # keep the app usable without a log file
            logger.addHandler(handler)
            return logger
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def get_logger():
    """Return the application logger (call setup_logger first)."""
    return logging.getLogger(LOGGER_NAME)
