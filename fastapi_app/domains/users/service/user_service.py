from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.domains.users.repository.user_repo import UserRepository
from fastapi_app.domains.users.schemas.user import UserCreate
from fastapi_app.domains.users.models.user import User
from fastapi_app.utils.hashing import hash_password


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(self, session: AsyncSession, data: UserCreate) -> User:
        """
        Создание нового пользователя.
        Проверяем уникальность email.
        Хэшируем пароль.
        """
        existing = await self.repo.get_by_email(session, data.email)
        if existing:
            raise ValueError("User already exists")

        user = User(
            email=data.email.lower().strip(),
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
        )
        return await self.repo.create(session, user)

    async def get_all(self, session: AsyncSession) -> list[User]:
        """Вернуть всех пользователей (в будущем будет пагинация)."""
        return await self.repo.get_all(session)
