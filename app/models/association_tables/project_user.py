from sqlalchemy import Table, Column, ForeignKey

from app.models import BaseModel

project_user = Table(
    "project_user",
    BaseModel.metadata,
    Column("project_id", ForeignKey("project.id"), primary_key=True),
    Column("user_id", ForeignKey("user.id"), primary_key=True),
)
