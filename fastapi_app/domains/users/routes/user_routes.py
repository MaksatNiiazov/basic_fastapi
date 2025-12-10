from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.core.db import get_session
from fastapi_app.domains.users.schemas.user import UserCreate, UserRead
from fastapi_app.domains.users.service.user_service import UserService
from fastapi_app.domains.users.deps import get_user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
        data: UserCreate,
        session: AsyncSession = Depends(get_session),
        service: UserService = Depends(get_user_service),
):
    try:
        user = await service.create_user(session, data)
        return user
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get("/", response_model=list[UserRead])
async def get_all_users(
        session: AsyncSession = Depends(get_session),
        service: UserService = Depends(get_user_service),
):
    return await service.get_all(session)
