from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from core.models.base import Base


class Permission(Base):
    __abstract__ = False

    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(255))
