from typing import AsyncGenerator

import aioredis

from app.settings.config_app import settings


async def redis_pool_factory() -> AsyncGenerator[aioredis.Redis, None]:
    """Создает и возвращает асинхронный пул соединений с Redis."""
    redis_pool = await aioredis.create_redis_pool(
        settings.REDIS_URL,
        maxsize=settings.REDIS_POOL,
        timeout=settings.REDIS_POOL_TIMEOUT
    )
    yield redis_pool
    redis_pool.close()
