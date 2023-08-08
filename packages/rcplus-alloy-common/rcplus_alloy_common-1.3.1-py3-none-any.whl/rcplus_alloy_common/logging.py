__all__ = [
    "configure_logger",
    "configure_new_logger",
    "configure_existing_logger",
    "configure_existing_loggers",
    "logger",
]

import logging
import os
from datetime import datetime, timezone
from typing import Union

from pythonjsonlogger import jsonlogger

from rcplus_alloy_common.constants import (
    LOGGING_DATETIME_FORMAT,
    LOGGING_FORMAT,
    LOG_LEVEL,
    LOG_MODE,
    LOG_NAME,
)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def formatTime(self, record, datefmt=None):
        return f"{datetime.fromtimestamp(record.created, tz=timezone.utc).strftime(LOGGING_DATETIME_FORMAT)[:-3]}Z"

    def process_log_record(self, log_record):
        dag_id = os.getenv("DAG_ID")
        if dag_id is not None:
            log_record["dag_id"] = dag_id
        dag_run_id = os.getenv("DAG_RUN_ID")
        if dag_run_id is not None:
            log_record["dag_run_id"] = dag_run_id
        aws_lambda_function_name = os.getenv("AWS_LAMBDA_FUNCTION_NAME")
        if aws_lambda_function_name is not None:
            log_record["origin"] = f"lambda/{aws_lambda_function_name}"
        env = os.getenv("ENVIRONMENT")
        if env is not None:
            log_record["env"] = env
        version = os.getenv("VERSION")
        if version is not None:
            log_record["version"] = version
        repository = os.getenv("REPOSITORY")
        if repository is not None:
            log_record["repository"] = repository
        software_component = os.getenv("SOFTWARE_COMPONENT")
        if software_component is not None:
            log_record["software_component"] = software_component
        return super().process_log_record(log_record)


class CustomLoggingFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        return f"{datetime.fromtimestamp(record.created, tz=timezone.utc).strftime(LOGGING_DATETIME_FORMAT)[:-3]}Z"


class AlloyStreamHandler(logging.StreamHandler):
    def __init__(self, *args, log_mode=LOG_MODE, **kwargs):
        super().__init__(*args, **kwargs)
        if log_mode == "JSON":
            self.setFormatter(
                CustomJsonFormatter(LOGGING_FORMAT, rename_fields={"levelname": "level", "asctime": "time"})
            )
        else:
            self.setFormatter(CustomLoggingFormatter(LOGGING_FORMAT))


def configure_new_logger(*args, **kwargs) -> logging.Logger:
    return configure_logger(*args, **kwargs)


def remove_custom_handlers(logger: logging.Logger) -> None:
    for handler in logger.handlers:
        if isinstance(handler, AlloyStreamHandler):
            logger.removeHandler(handler)


def configure_logger(
    log_name: str = LOG_NAME,
    log_mode: str = LOG_MODE,
    log_level: Union[str, int] = LOG_LEVEL,
    capture_warnings: bool = True,
) -> logging.Logger:
    """
    Configure the root logger and return a new logger with the given name.
    """
    logging.captureWarnings(capture_warnings)
    handler = create_handler(log_mode)
    remove_custom_handlers(logging.root)
    logging.root.addHandler(handler)

    new_logger = logging.getLogger(log_name)
    new_logger.setLevel(log_level)
    return new_logger


def create_handler(log_mode: str = LOG_MODE) -> logging.Handler:
    return AlloyStreamHandler(log_mode=log_mode)


def configure_existing_loggers(
    log_level: Union[str, int] = LOG_LEVEL,
    log_name_filter: str | None = None,
) -> dict[logging.Logger, int]:
    """
    Configure all existing loggers to be the same (output as text/json, level) or
    configure only some specific 3rd party loggers (like urllib3 etc.) using log_name_filter.
    """
    # logging.captureWarnings(capture_warnings)
    prev_state = {}

    for log_name in logging.root.manager.loggerDict:
        if log_name_filter is not None and log_name_filter not in log_name:
            continue
        existing_logger = logging.getLogger(log_name)
        prev_state[existing_logger] = existing_logger.getEffectiveLevel()
        configure_existing_logger(existing_logger, log_level)
    return prev_state


def configure_existing_logger(
    existing_logger: logging.Logger,
    log_level: Union[str, int] = LOG_LEVEL,
) -> None:
    """
    (Re-)Configure an existing logger.
    """
    existing_logger.setLevel(log_level)


# The default utility logger.
logger = configure_logger(log_name=str(os.path.basename(__file__).split(".")[0]))
