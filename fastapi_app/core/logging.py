import os
from datetime import datetime
from logging.config import dictConfig
from fastapi_app.core.config import settings


def setup_logging() -> None:
    cfg = settings.logging

    handlers = {}
    root_handlers = []

    # === Console handler ===
    if cfg.console_enabled:
        handlers["console"] = {
            "class": "logging.StreamHandler",
            "formatter": "default",
        }
        root_handlers.append("console")

    if cfg.file_enabled:
        now = datetime.now()
        year = str(now.year)
        month = f"{now.month:02d}"
        day = f"{now.day:02d}"

        # Берём базовую директорию из конфигурации
        base_logs = cfg.base_dir

        # Полный путь со структурой logs/YYYY/MM/DD/
        dated_dir = os.path.join(base_logs, year, month, day)
        os.makedirs(dated_dir, exist_ok=True)

        # Файл задаётся ТОЛЬКО именем
        file_name = os.path.basename(cfg.file_name)

        # Получаем итоговый путь
        full_path = os.path.join(dated_dir, file_name)

        handlers["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": full_path,
            "maxBytes": cfg.file_max_bytes,
            "backupCount": cfg.file_backup_count,
            "encoding": "utf-8",
        }

        root_handlers.append("file")
    # === Uvicorn access formatter ===
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
                    "handlers": root_handlers,
                    "level": cfg.level,
                    "propagate": False,
                },

                "sqlalchemy.engine": {
                    "handlers": root_handlers,
                    "level": "WARNING",
                    "propagate": False,
                },

                "request_logger": {
                    "handlers": root_handlers,
                    "level": cfg.level,
                    "propagate": False,
                },
            },

            "root": {
                "handlers": root_handlers,
                "level": cfg.level,
            },
        }
    )
