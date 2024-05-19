from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.types import LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import BaseModel
from app.models.role import UserRoles

if TYPE_CHECKING:
    from app.models import Role, Project


class User(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(LargeBinary())
    role_name: Mapped[UserRoles] = mapped_column(ForeignKey("role.name"))

    role: Mapped["Role"] = relationship(
        back_populates="users",
    )
    projects: Mapped[list["Project"]] = relationship(
        back_populates="owner",

    )
    join_requests: Mapped[list["Project"]] = relationship(
        secondary="user_join_project_request",
        back_populates="join_requests",
    )
    joined_projects: Mapped[list["Project"]] = relationship(
        secondary="project_user",
        back_populates="members",
    )

    def __str__(self):
        return f"User(id={self.id}, email={self.email}, role_name={self.role_name})"

    def __repr__(self):
        return str(self)
