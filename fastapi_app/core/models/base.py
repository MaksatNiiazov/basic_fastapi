from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from fastapi_app.core.config import settings
from fastapi_app.utils.naming import make_tablename


class Base(DeclarativeBase):
    __abstract__ = True

    def __tablename__(cls) -> str:
        return make_tablename(cls)

    id: Mapped[int] = mapped_column(primary_key=True)

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )
