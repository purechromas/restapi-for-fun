from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.models import Permission
from app.infra.postgres import get_async_session, base_model


async def add_tables_permissions_names():
    """
    Автоматически добавляет имена прав для всех таблиц в базу данных.
    """
    tables_names = list(base_model.metadata.tables.keys())
    async for session in get_async_session():
        for table_name in tables_names:
            perms_names = [
                f"{table_name}_read",
                f"{table_name}_create",
                f"{table_name}_update",
                f"{table_name}_delete",
            ]
            for name in perms_names:
                stmt = insert(Permission).values(name=name).on_conflict_do_nothing()
                await session.execute(stmt)
        await session.commit()


async def get_permissions_by_names(permission_names: set) -> list[Permission]:
    """
    Возвращает список прав по заданным именам.
    """
    async for session in get_async_session():
        results = await session.execute(
            select(Permission).where(Permission.name.in_(permission_names))
        )
        permissions = results.scalars().all()
        return permissions
