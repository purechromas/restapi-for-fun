from app.infra.postgres import get_async_session
from app.models import Group
from app.models.group import DefaultGroups


async def create_default_project_groups(project_id: int) -> tuple[Group, Group]:
    """Создает и возвращает группы - участников и администраторов по умолчанию для проекта."""
    async for session in get_async_session():
        with session.begin():
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
