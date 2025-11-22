import os
from datetime import datetime
from logging.config import dictConfig
from fastapi_app.core.config import settings


def setup_logging() -> None:
    cfg = settings.logging

    handlers = {}
    service_handlers = []
    request_handlers = []

    # === Console handler ===
    if cfg.console_enabled:
        handlers["console"] = {
            "class": "logging.StreamHandler",
            "formatter": "default",
        }
        service_handlers.append("console")
        request_handlers.append("console")

    if cfg.file_enabled:
        now = datetime.now()
        year = str(now.year)
        month = f"{now.month:02d}"
        day = f"{now.day:02d}"

        base_logs = cfg.base_dir

        # Service file handler
        service_dated_dir = os.path.join(base_logs, cfg.services_dir, year, month, day)
        os.makedirs(service_dated_dir, exist_ok=True)

        service_full_path = os.path.join(service_dated_dir, cfg.service_file_name)

        handlers["service_file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": service_full_path,
            "maxBytes": cfg.file_max_bytes,
            "backupCount": cfg.file_backup_count,
            "encoding": "utf-8",
        }
        service_handlers.append("service_file")

        # Request file handler
        request_dated_dir = os.path.join(base_logs, cfg.request_dir, year, month, day)
        os.makedirs(request_dated_dir, exist_ok=True)

        request_full_path = os.path.join(request_dated_dir, cfg.request_file_name)

        handlers["request_file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": request_full_path,
            "maxBytes": cfg.file_max_bytes,
            "backupCount": cfg.file_backup_count,
            "encoding": "utf-8",
        }
        request_handlers.append("request_file")

    handlers["uvicorn_console"] = {
        "class": "logging.StreamHandler",
        "formatter": "uvicorn",
    }

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,

            "formatters": {
                "default": {
                    "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                },
                "uvicorn": {
                    "()": "uvicorn.logging.AccessFormatter",
                    "fmt": "%(levelprefix)s %(client_addr)s - \"%(request_line)s\" %(status_code)s",
                }
            },

            "handlers": handlers,

            "loggers": {
                "uvicorn.access": {
                    "handlers": ["uvicorn_console"],
                    "level": "INFO",
                    "propagate": False,
                },

                "uvicorn.error": {
                    "handlers": service_handlers,
                    "level": cfg.level,
                    "propagate": False,
                },

                "sqlalchemy.engine": {
                    "handlers": service_handlers,
                    "level": "WARNING",
                    "propagate": False,
                },

                "request_logger": {
                    "handlers": request_handlers,
                    "level": cfg.level,
                    "propagate": False,
                },
            },

            "root": {
                "handlers": service_handlers,
                "level": cfg.level,
            },
        }
    )