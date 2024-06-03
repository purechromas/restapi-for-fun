from app.exceptions.api_exceptions import TokenNotExist
from app.infra.redis import get_redis_pool


async def set_access_token_cache(access_token: str, email: str, expire_minutes: int):
    """
     Устанавливает кэш доступа для токена в Redis.

     Параметры:
     - access_token (str): Токен доступа.
     - email (str): Адрес электронной почты пользователя.
     - expire_minutes (int): Время жизни кэша в минутах.
     """
    expire_seconds = expire_minutes * 60

    async for redis in get_redis_pool():
        await redis.set(access_token, email, expire=expire_seconds)


async def get_access_token_cache(access_token: str) -> str:
    """
      Получает кэш доступа для указанного токена из Redis.

      Параметры:
      - access_token (str): Токен доступа.

      Возвращает:
      - str: Адрес электронной почты, связанный с указанным токеном доступа.

      Исключения:
      - TokenNotExist: Если кэш для указанного токена не существует.
      """
    async for redis in get_redis_pool():
        cached_access_token: bytes = await redis.get(access_token)

        if not cached_access_token:
            raise TokenNotExist

        return cached_access_token.decode()
