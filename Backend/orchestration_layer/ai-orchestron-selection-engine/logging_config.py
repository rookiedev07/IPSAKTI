"""
Central logging setup for the engine. Every decision the engine makes gets
written to logs/engine.log (and echoed to the console) so you can show a
judge -- or debug yourself -- *why* a specific model was picked for a
specific prompt, without needing to re-run anything.

Usage, anywhere in the project:
    from logging_config import get_logger
    logger = get_logger()
    logger.info("something happened")
"""

import logging
import os
from logging.handlers import RotatingFileHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "engine.log")


def get_logger(name: str = "ai_orchestron") -> logging.Logger:
    logger = logging.getLogger(name)

    # If handlers already exist, this logger was already configured
    # elsewhere (e.g. imported by both main.py and server.py) -- don't
    # attach duplicate handlers or every line will print twice.
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=1_000_000, backupCount=3
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False

    return logger
