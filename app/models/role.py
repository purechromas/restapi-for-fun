import enum
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import BaseModel

if TYPE_CHECKING:
    from app.models import User, Permission


class UserRoles(str, enum.Enum):
    SUPERUSER = "superuser"  # Владелец сервиса - DB KEY | PROGRAM VALUE
    ADMIN = "admin"  # Администраторы сервиса - DB KEY | PROGRAM VALUE
    USER = "user"  # Пользователь сервиса - DB KEY | PROGRAM VALUE


class Role(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[UserRoles] = mapped_column(unique=True)

    users: Mapped[list["User"]] = relationship(
        back_populates="role",
    )
    permissions: Mapped[list["Permission"]] = relationship(
        secondary="role_permission",
        back_populates="roles",
    )

    def __str__(self):
        return f"Role(id={self.id}, name={self.name})"

    def __repr__(self):
        return str(self)
