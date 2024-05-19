from sqlalchemy import insert

from app.models import project_user
from app.settings.postgres import get_async_session


async def add_new_user_in_project(project_id: int, user_id: int):
    async for session in get_async_session():
        await session.execute(
            insert(project_user).values(
                project_id=project_id,
                user_id=user_id
            )
        )
        await session.commit()
