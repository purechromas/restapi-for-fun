from sqlalchemy import Table, Column, ForeignKey

from app.models import BaseModel

role_permission = Table(
    "role_permission",
    BaseModel.metadata,
    Column("role_id", ForeignKey("role.id"), primary_key=True),
    Column("permission_id", ForeignKey("permission.id"), primary_key=True),
)
