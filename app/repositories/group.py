from app.models import Group
from app.models.group import DefaultGroups
from app.settings.postgres import get_async_session


async def create_default_project_groups(project_id: int) -> tuple[Group, Group]:
    """
    Создает и возвращает группы - участников и администраторов по умолчанию для проекта.
    """
    async for session in get_async_session():
        member = Group(
            name=DefaultGroups.MEMBER,
            project_id=project_id
        )
        administrator = Group(
            name=DefaultGroups.ADMINISTRATOR,
            project_id=project_id
        )

        session.add(member)
        session.add(administrator)
        await session.commit()

        await session.refresh(member)
        await session.refresh(administrator)

        return member, administrator
