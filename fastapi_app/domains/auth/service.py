from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from fastapi_app.domains.auth.schemas import LoginRequest, RefreshRequest, TokenPair
from fastapi_app.domains.users.models.user import User
from fastapi_app.domains.users.repository.user_repo import UserRepository
from fastapi_app.utils.hashing import verify_password


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def login(self, session: AsyncSession, data: LoginRequest) -> TokenPair:
        user = await self.user_repo.get_by_email(session, data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise ValueError("Invalid credentials")

        if not user.is_active:
            raise ValueError("User is inactive")

        access = create_access_token(subject=user.id)
        refresh = create_refresh_token(subject=user.id)
        return TokenPair(access_token=access, refresh_token=refresh)

    async def refresh(self, session: AsyncSession, data: RefreshRequest) -> TokenPair:
        payload = decode_token(data.refresh_token)

        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type")

        user_id = int(payload["sub"])
        user: User | None = await session.get(User, user_id)

        if not user or not user.is_active:
            raise ValueError("User not found or inactive")

        access = create_access_token(subject=user.id)
        refresh = create_refresh_token(subject=user.id)
        return TokenPair(access_token=access, refresh_token=refresh)
