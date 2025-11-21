import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_app.core.config import settings

logger = logging.getLogger(__name__)


def setup_cors(app: FastAPI) -> None:
    cors_cfg = settings.cors

    logger.info(
        "Configuring CORS middleware",
        extra={
            "allow_origins": cors_cfg.allow_origins,
            "allow_methods": cors_cfg.allow_methods,
            "allow_headers": cors_cfg.allow_headers,
            "allow_credentials": cors_cfg.allow_credentials,
        }
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_cfg.allow_origins,
        allow_credentials=cors_cfg.allow_credentials,
        allow_methods=cors_cfg.allow_methods,
        allow_headers=cors_cfg.allow_headers,
    )
