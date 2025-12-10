# fastapi_app/domains/auth/routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.core.db import get_session
from fastapi_app.domains.auth.deps import get_current_user
from fastapi_app.domains.auth.schemas import (
    LoginRequest,
    RefreshRequest,
    TokenPair,
)
from fastapi_app.domains.auth.service import AuthService
from fastapi_app.domains.users.deps import get_user_repo
from fastapi_app.domains.users.models.user import User
from fastapi_app.domains.users.repository.user_repo import UserRepository
from fastapi_app.domains.users.schemas.user import UserRead

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_auth_service(
        user_repo: UserRepository = Depends(get_user_repo),
) -> AuthService:
    return AuthService(user_repo)


@router.post("/login", response_model=TokenPair)
async def login(
        data: LoginRequest,
        session: AsyncSession = Depends(get_session),
        service: AuthService = Depends(get_auth_service),
):
    try:
        return await service.login(session, data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )


@router.post("/refresh", response_model=TokenPair)
async def refresh(
        data: RefreshRequest,
        session: AsyncSession = Depends(get_session),
        service: AuthService = Depends(get_auth_service),
):
    try:
        return await service.refresh(session, data)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )


@router.get("/me", response_model=UserRead)
async def me(current_user: User = Depends(get_current_user)):
    return current_user
