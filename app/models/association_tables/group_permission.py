from sqlalchemy import Table, Column, ForeignKey

from app.models import BaseModel

group_permission = Table(
    "group_permission",
    BaseModel.metadata,
    Column("group_id", ForeignKey("group.id"), primary_key=True),
    Column("permission_id", ForeignKey("permission.id"), primary_key=True),
)
