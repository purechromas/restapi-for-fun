from sqlalchemy.dialects.postgresql import insert

from app.models.role import UserRoles, Role
from app.settings.postgres import get_async_session


async def add_system_roles():
    """
    Добавляет системные роли в базу данных, если они еще не существуют.
    """
    async for session in get_async_session():
        for role in UserRoles:
            insert_stmt = insert(Role).values(name=role)
            do_nothing_stmt = insert_stmt.on_conflict_do_nothing()
            await session.execute(do_nothing_stmt)
        await session.commit()
