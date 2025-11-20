import os
from logging.config import dictConfig


def setup_logging() -> None:
    os.makedirs("logs", exist_ok=True)

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,

            # === FORMATTERS ===
            "formatters": {
                "default": {
                    "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                },
                "uvicorn": {
                    "format": "%(levelprefix)s %(message)s",
                },
            },

            # === HANDLERS ===
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                },

                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "default",
                    "filename": "logs/app.log",
                    "maxBytes": 10_000_000,
                    "backupCount": 5,
                    "encoding": "utf-8",
                },

                "uvicorn_console": {
                    "class": "logging.StreamHandler",
                    "formatter": "uvicorn",
                },
            },

            # === SPECIFIC LOGGERS ===
            "loggers": {
                "uvicorn.access": {
                    "handlers": ["uvicorn_console"],
                    "level": "INFO",
                    "propagate": False,
                },

                "uvicorn.error": {
                    "level": "INFO",
                    "handlers": ["console"],
                    "propagate": False,
                },

                "sqlalchemy.engine": {
                    "level": "WARNING",
                    "handlers": ["console", "file"],
                    "propagate": False,
                },
                "request_logger": {
                    "handlers": ["console", "file"],
                    "level": "INFO",
                    "propagate": False,
                },
            },

            # === ROOT LOGGER (логи приложения) ===
            "root": {
                "handlers": ["console", "file"],
                "level": "INFO",
            },
        }
    )
