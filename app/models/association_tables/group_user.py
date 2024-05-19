from sqlalchemy import Table, Column, ForeignKey

from app.models import BaseModel

group_user = Table(
    "group_user",
    BaseModel.metadata,
    Column("group_id", ForeignKey("group.id"), primary_key=True),
    Column("user_id", ForeignKey("user.id"), primary_key=True),
)
