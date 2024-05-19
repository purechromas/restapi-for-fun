from sqlalchemy import select, insert, Row

from app.exceptions import ProjectAlreadyExist
from app.models import Project
from app.settings.postgres import get_async_session


async def create_project_if_not_exist(project_data: dict) -> Project:
    """
    Создает проект, если он не существует. Если проект с таким именем уже существует,
    выбрасывает исключение ProjectAlreadyExist.
    """
    async for session in get_async_session():
        stmt = select(Project).where(Project.name == project_data["name"])
        result = await session.execute(stmt)

        if result.scalar_one_or_none():
            raise ProjectAlreadyExist

        project = Project(
            name=project_data["name"],
            description=project_data.get("description"),
            owner_id=project_data["owner_id"]
        )
        session.add(project)
        await session.commit()
        await session.refresh(project)

        return project
