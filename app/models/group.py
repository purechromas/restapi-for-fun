import enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import BaseModel

if TYPE_CHECKING:
    from app.models import User, Permission, Project


class DefaultGroups(enum.Enum):
    """
    Стандартные группы для каждого нового проекта.
    У каждой группы есть свои собственные права доступа.
    """
    ADMINISTRATOR = "administrator"  # администратор проекта
    MEMBER = "member"  # участник проекта


class Group(BaseModel):
    """
     ВАЖНО:
         Может существовать несколько групп с одинаковым именем в разных проектах,
         но идентификаторы проектов будут различными.
     ПРИМЕР:
         ГРУППА 1 - имя=member, project_id=1
         ГРУППА 2 - имя=member, project_id=2
     """
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[DefaultGroups] = mapped_column(Enum(DefaultGroups))
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))

    members: Mapped[list["User"]] = relationship(
        secondary="group_user",
    )
    project: Mapped["Project"] = relationship(
        back_populates="groups"
    )
    permissions: Mapped[list["Permission"]] = relationship(
        secondary="group_permission",
        back_populates="groups"
    )

    def __str__(self):
        return f"Group(id={self.id}, name={self.name})"

    def __repr__(self):
        return str(self)
