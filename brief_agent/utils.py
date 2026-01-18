"""Utility functions for logging and helpers."""

import logging
import os
from datetime import datetime
from pathlib import Path


def setup_logging(log_dir: Path | str = "logs", level: str | None = None) -> logging.Logger:
    """
    Set up logging with file and console handlers.

    Args:
        log_dir: Directory for log files
        level: Logging level (defaults to LOG_LEVEL env var or INFO)

    Returns:
        Configured logger instance
    """
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    # Get log level from env or parameter
    level_str = level or os.getenv("LOG_LEVEL", "INFO")
    log_level = getattr(logging, level_str.upper(), logging.INFO)

    # Create logger
    logger = logging.getLogger("brief_agent")
    logger.setLevel(log_level)

    # Clear existing handlers
    logger.handlers.clear()

    # File handler
    log_file = log_dir / f"run_{datetime.now().strftime('%Y-%m-%d')}.log"
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(log_level)
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger


def get_logger() -> logging.Logger:
    """Get the brief_agent logger."""
    return logging.getLogger("brief_agent")


def ensure_directory(path: Path | str) -> Path:
    """Ensure a directory exists, creating it if necessary."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def format_date(date_str: str) -> str:
    """Ensure date is in YYYY-MM-DD format."""
    try:
        parsed = datetime.strptime(date_str, "%Y-%m-%d")
        return parsed.strftime("%Y-%m-%d")
    except ValueError:
        # Try other common formats
        for fmt in ["%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d"]:
            try:
                parsed = datetime.strptime(date_str, fmt)
                return parsed.strftime("%Y-%m-%d")
            except ValueError:
                continue
        return date_str  # Return as-is if parsing fails
