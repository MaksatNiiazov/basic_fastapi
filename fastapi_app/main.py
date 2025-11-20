from contextlib import asynccontextmanager

from fastapi import FastAPI

from api import api_router
from core.config import settings
from core.cors import setup_cors
from core.exceptions import setup_exception_handlers
from core.logging import setup_logging
from core.models import db_helper
from middleware.request_logger import RequestLoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title="FastAPI Base Template",
        version="1.0.0",
        lifespan=lifespan,
    )
    setup_cors(app)
    app.add_middleware(RequestLoggingMiddleware)

    setup_exception_handlers(app)

    # Маршруты
    app.include_router(api_router, prefix=settings.api.prefix)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )
