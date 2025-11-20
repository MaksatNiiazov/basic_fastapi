from contextlib import asynccontextmanager
from fastapi import FastAPI

from fastapi_app.api import api_router
from fastapi_app.core.config import settings
from fastapi_app.core.models import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


app = FastAPI(
    lifespan=lifespan
)
app.include_router(
    api_router,
    prefix=settings.api.prefix,
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )
