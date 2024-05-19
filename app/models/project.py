from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import BaseModel

if TYPE_CHECKING:
    from app.models import User, Group


class Project(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[str | None]
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    owner: Mapped["User"] = relationship(
        back_populates="projects",
    )
    members: Mapped[list["User"]] = relationship(
        secondary="project_user",
        back_populates="joined_projects",
    )
    groups: Mapped[list["Group"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan"
    )
    join_requests: Mapped[list["User"]] = relationship(
        secondary="user_join_project_request",
        back_populates="join_requests",
    )

    def __str__(self):
        return f"Project(id={self.id}, name={self.name}), description={self.description}"

    def __repr__(self):
        return str(self)
