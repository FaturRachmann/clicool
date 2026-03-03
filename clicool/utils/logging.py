"""Logging utilities for clicool."""

import logging
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler

from .. import CLICOOL_HOME

console = Console()


class ClicoolLogger:
    """Logger for clicool."""

    LOG_FILE = CLICOOL_HOME / "clicool.log"

    @classmethod
    def get_logger(
        cls,
        name: str = "clicool",
        level: int = logging.INFO,
        use_rich: bool = True,
    ) -> logging.Logger:
        """
        Get a logger instance.

        Args:
            name: Logger name
            level: Logging level
            use_rich: Use Rich handler for pretty output

        Returns:
            Configured logger
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Avoid duplicate handlers
        if logger.handlers:
            return logger

        # Ensure log directory exists
        cls.LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

        if use_rich:
            # Rich console handler
            handler = RichHandler(
                console=console,
                rich_tracebacks=True,
                tracebacks_show_locals=False,
                markup=True,
            )
            handler.setLevel(level)
            logger.addHandler(handler)
        else:
            # Standard stream handler
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(level)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="[%X]",
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        # File handler
        try:
            file_handler = logging.FileHandler(cls.LOG_FILE)
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except Exception:
            # If we can't write to log file, continue without it
            pass

        return logger


def get_logger(
    name: str = "clicool",
    level: int = logging.INFO,
) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name
        level: Logging level

    Returns:
        Configured logger
    """
    return ClicoolLogger.get_logger(name, level)


class LoggerContext:
    """Context manager for logging."""

    def __init__(
        self,
        logger: logging.Logger,
        message: str,
        success_message: Optional[str] = None,
        error_message: Optional[str] = None,
    ):
        """
        Initialize logging context.

        Args:
            logger: Logger instance
            message: Message to log at start
            success_message: Message to log on success
            error_message: Message to log on error
        """
        self.logger = logger
        self.message = message
        self.success_message = success_message
        self.error_message = error_message

    def __enter__(self):
        self.logger.info(self.message)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            if self.success_message:
                self.logger.info(self.success_message)
        else:
            if self.error_message:
                self.logger.error(f"{self.error_message}: {exc_val}")
            else:
                self.logger.error(f"Error: {exc_val}")
        return False


def log_operation(
    logger: logging.Logger,
    operation: str,
    success: bool,
    details: Optional[str] = None,
):
    """
    Log an operation result.

    Args:
        logger: Logger instance
        operation: Operation name
        success: Whether operation succeeded
        details: Optional details
    """
    if success:
        logger.info(f"✓ {operation}")
    else:
        logger.error(f"✗ {operation}")

    if details:
        logger.debug(details)


__all__ = [
    "ClicoolLogger",
    "get_logger",
    "LoggerContext",
    "log_operation",
]
