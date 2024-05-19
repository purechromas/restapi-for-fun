from sqlalchemy import Table, Column, ForeignKey

from app.models import BaseModel

user_join_project_request = Table(
    "user_join_project_request",
    BaseModel.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("project_id", ForeignKey("project.id"), primary_key=True),
)
