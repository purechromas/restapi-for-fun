import logging

from fastapi import HTTPException, status

from app.web.api_v1.project.schemas import ProjectCreateIn, ProjectCreateOut
from app.exceptions.repo_exceptions import ProjectExistError
from app.models import User, Project, Group
from app.repositories.group import create_default_project_groups
from app.repositories.group_permission import create_default_group_permissions
from app.repositories.project import create_project_if_not_exist
from app.repositories.project_user import add_new_user_in_project
from app.settings.config_app import settings

log = logging.getLogger(settings.APP_NAME)


async def process_create_project_request(
        user: User,
        body_data: ProjectCreateIn
) -> ProjectCreateOut:
    """
      Обрабатывает запрос на создание проекта.

      Параметры:
      - user (User): Пользователь, инициирующий запрос.
      - body_data (ProjectCreateIn): Данные для создания проекта из запроса.

      Возвращает:
      - ProjectCreateOut: Ответное сообщение с информацией о созданном проекте.

      Исключения:
      - ProjectAlreadyExist: Если проект с таким именем уже существует.
      """
    project_data = {
        "name": body_data.name,
        "description": body_data.description,
        "owner_id": user.id
    }
    try:
        project: Project = await create_project_if_not_exist(project_data)
        await add_new_user_in_project(project.id, user.id)
        groups: tuple[Group, Group] = await create_default_project_groups(project.id)
        await create_default_group_permissions(groups)
        return ProjectCreateOut(id=project.id, name=project.name, description=project.description)
    except ProjectExistError:
        log.error(f"ProjectAlreadyExist: {project_data['name']}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project with that name already exist, try with another."
        )
