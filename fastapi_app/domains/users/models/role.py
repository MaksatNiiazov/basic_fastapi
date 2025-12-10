from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from core.models.base import Base
from .permission import Permission
from .role_permission import RolePermission


class Role(Base):
    __abstract__ = False

    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str | None] = mapped_column(String(255))

    permissions: Mapped[list[Permission]] = relationship(
        secondary="role_permission",
        lazy="joined"
    )
