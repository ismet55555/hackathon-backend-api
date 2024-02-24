"""Setting up logger for application."""

import logging
from logging import Logger
from logging.handlers import RotatingFileHandler
from os import getenv

# from logging_tree import printout


def get_logger(
    log_level: str = "info",
    log_file_enabled: bool = True,
    log_filename: str = "backend_api.log",
) -> Logger:
    """Set up FastAPI specific logger setup.

    Args:
        log_level: Level of logging
        log_file_enabled: Set True if logging to a specific file
        log_filename: Name of the log file

    Returns:
        Configured logging object
    """
    logger_name = "uvicorn" if getenv("APP_ENV") == "dev" else "gunicorn"
    log_level = getenv("LOG_LEVEL", log_level)

    # Setting logging level
    log_format = "[%(asctime)s] [%(levelname)-8s] %(message)s"
    if log_level.lower() == "debug":
        level = logging.DEBUG
        log_format = "[%(asctime)s] [%(levelname)-8s] [%(filename)-24s:%(lineno)4s] %(message)s"
    elif log_level.lower() == "warning":
        level = logging.WARNING
    else:
        level = logging.INFO

    # Turn off INFO level logging for specific python packages
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("dicttoxml").setLevel(logging.WARNING)
    logging.getLogger("boto").setLevel(logging.WARNING)
    logging.getLogger("botocore").setLevel(logging.WARNING)

    # Set logger depending on environment
    log = logging.getLogger(logger_name)

    # Add any additional handlers
    if log_file_enabled:
        log.addHandler(
            RotatingFileHandler(
                filename=log_filename,
                mode="a",
                maxBytes=5000000,
                backupCount=0,
                delay=True,
                encoding="utf-8",
            )
        )

        # Set Logging level and formatting for all handlers
        log.setLevel(level)
        formatter = logging.Formatter(log_format, datefmt="%H:%M:%S")
        for handler in log.handlers:
            handler.setFormatter(formatter)

        log.debug(
            f'Successfully set up message logger "{logger_name}". '
            f"Logging level {log_level} ({level}). "
            f"Logging to local file: {log_file_enabled}"
        )

    # printout()
    return log
