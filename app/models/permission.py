from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import BaseModel

if TYPE_CHECKING:
    from app.models import Role, Group


class Permission(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)

    # atm in service we don't use this relationship
    roles: Mapped[list["Role"]] = relationship(
        secondary="role_permission",
        back_populates="permissions",
    )
    groups: Mapped[list["Group"]] = relationship(
        secondary="group_permission",
        back_populates="permissions"
    )

    def __str__(self):
        return f"Permission(id={self.id}, name={self.name})"

    def __repr__(self):
        return str(self)
