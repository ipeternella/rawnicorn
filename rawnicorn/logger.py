"""
Logging setup for Rawunicorn.
"""
import logging
from typing import Dict


class LogLevelColorFormatter(logging.Formatter):
    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"

    # formats
    fmt = "%(asctime)s [%(process)d] [%(levelname)s] %(message)s"

    FORMATS = {
        logging.DEBUG: grey + fmt,
        logging.INFO: grey + fmt,
        logging.WARNING: yellow + fmt,
        logging.ERROR: red + fmt,
        logging.CRITICAL: bold_red + fmt,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        datefmt = "%Y-%m-%d %H:%M:%S %z"

        formatter = logging.Formatter(fmt=log_fmt, datefmt=datefmt)
        return formatter.format(record)


def build_logging_config(level: str) -> Dict:
    return {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "standard": {
                "class": "rawnicorn.logger.LogLevelColorFormatter",
            },
        },
        "handlers": {
            "stdout_handler": {"class": "logging.StreamHandler", "formatter": "standard", "stream": "ext://sys.stdout"},
            "stderr_handler": {"class": "logging.StreamHandler", "formatter": "standard", "stream": "ext://sys.stderr"},
        },
        "loggers": {
            "": {
                "handlers": ["stdout_handler"],
                "level": level,
                "propagate": True,
            },  # root logger
            "rawnicorn.access": {
                "level": level,
                "propagate": True,  # propagates msgs to ancestor (root logger), no handler here
            },
            "rawnicorn.error": {
                "handlers": ["stderr_handler"],
                "level": level,
                "propagate": False,  # no root logger usage -> uses stderr stream
            },
        },
    }
