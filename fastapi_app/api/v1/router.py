from fastapi import APIRouter

from fastapi_app.domains.auth.routes import router as auth_router
from fastapi_app.domains.users.routes.user_routes import router as users_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(users_router)
