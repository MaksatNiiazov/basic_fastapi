from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.domains.users.models.user import User


class UserRepository:

    @staticmethod
    async def get_by_email(session: AsyncSession, email: str) -> User | None:
        stmt = select(User).where(User.email.ilike(email))
        res = await session.execute(stmt)
        return res.scalar_one_or_none()

    @staticmethod
    async def get(session: AsyncSession, user_id: int) -> User | None:
        return await session.get(User, user_id)

    @staticmethod
    async def get_all(session: AsyncSession) -> list[User]:
        stmt = select(User).order_by(User.id)
        result = await session.scalars(stmt)
        return list(result.all())

    @staticmethod
    async def create(session: AsyncSession, user: User) -> User:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def update(session: AsyncSession, user: User, **fields) -> User:
        for key, value in fields.items():
            setattr(user, key, value)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def delete(session: AsyncSession, user_id: int) -> None:
        user = await session.get(User, user_id)
        if user is not None:
            await session.delete(user)
            await session.commit()
