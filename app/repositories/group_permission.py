from sqlalchemy import insert

from app.web.api_v1.project.default_permissions import (
    project_administrator_default_permissions,
    project_user_default_permissions,
)
from app.models import Group, group_permission
from app.models.group import DefaultGroups
from app.repositories.permission import get_permissions_by_names

from app.infra.postgres import get_async_session


async def create_default_group_permissions(groups: tuple[Group, Group]):
    """
    Создает права доступа по умолчанию для заданных групп проектов.
    """
    async for session in get_async_session():
        for group in groups:
            if group.name == DefaultGroups.ADMINISTRATOR:
                permissions = (
                    await get_permissions_by_names(project_administrator_default_permissions)
                )
                for perm in permissions:
                    stmt = insert(group_permission).values(
                        group_id=group.id,
                        permission_id=perm.id
                    )
                    await session.execute(stmt)
            elif group.name == DefaultGroups.MEMBER:
                permissions = (
                    await get_permissions_by_names(project_user_default_permissions)
                )
                for perm in permissions:
                    stmt = insert(group_permission).values(
                        group_id=group.id,
                        permission_id=perm.id
                    )
                    await session.execute(stmt)

            await session.commit()
