from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.models import BaseModel

from app.settings.config import settings


class PGHelper:
    """
    Класс для управления подключением к базе данных PostgreSQL.
    """

    def __init__(self, url: str, echo: bool = False, pool_size: int = 10, pool_timeout: int = 30):
        self._engine = create_async_engine(
            url=url, echo=echo, pool_size=pool_size, pool_timeout=pool_timeout
        )

    async def create_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Создает и возвращает асинхронную сессию SQLAlchemy.
        """
        async_session_maker = async_sessionmaker(self._engine, class_=AsyncSession)
        async with async_session_maker() as session:
            yield session
            await session.close()

    async def create_tables(self, base: DeclarativeBase):
        """
        Создает таблицы в базе данных на основе метаданных переданной базы данных.
        """
        async with self._engine.begin() as conn:
            await conn.run_sync(base.metadata.create_all)


base_model = BaseModel()
pg_helper = PGHelper(settings.PG_URL, settings.SQLALCHEMY_ECHO, settings.PG_POOL_TIMEOUT)
get_async_session = pg_helper.create_async_session
