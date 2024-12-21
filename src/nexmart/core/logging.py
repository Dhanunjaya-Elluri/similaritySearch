import logging
from typing import Any


def setup_logging() -> None:
    """Configure application logging.

    Sets up basic logging configuration with INFO level and a specific format.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def get_logger(name: str) -> Any:
    """Get a logger instance.

    Args:
        name (str): The name of the logger, typically __name__.

    Returns:
        Any: A logger instance configured with the application's settings.
    """
    return logging.getLogger(name)
