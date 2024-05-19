from typing import Annotated

from fastapi import APIRouter, Body, Depends, status

from app.api_v1.api_dependencies import authentication
from app.api_v1.project.dependencies import process_create_project_request
from app.api_v1.project.schemas import ProjectCreateIn, ProjectCreateOut
from app.models import User

project_routers = APIRouter(prefix="", tags=["Project, group, permission"])


@project_routers.post("/create_project/", status_code=status.HTTP_201_CREATED)
async def create_project(
        user: Annotated[User, Depends(authentication)],
        body_data: Annotated[ProjectCreateIn, Body()]
) -> ProjectCreateOut:
    return await process_create_project_request(user, body_data)


