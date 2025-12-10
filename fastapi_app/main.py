# main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI

from fastapi_app.api import api_router
from fastapi_app.core.config import settings
from fastapi_app.core.cors import setup_cors
from fastapi_app.core.exceptions import setup_exception_handlers
from fastapi_app.core.logging import setup_logging
from fastapi_app.core.models import db_helper
from fastapi_app.middleware.request_logger import RequestLoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI Base Template",
        version="1.0.0",
        lifespan=lifespan,
    )

    setup_cors(app)
    app.add_middleware(RequestLoggingMiddleware)
    setup_exception_handlers(app)
    app.include_router(api_router, prefix=settings.api.prefix)

    return app


app = create_app()


setup_logging()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_config=None)