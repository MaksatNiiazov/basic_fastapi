from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from core.models.base import Base


class RolePermission(Base):
    __abstract__ = False

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id"))
