import logging
from typing import Annotated

from fastapi import HTTPException, Header, status

from app.cache.cache_tokens import get_access_token_cache
from app.exceptions import TokenNotExist, UserNotExist
from app.models import User
from app.repositories.user import get_user_if_exist
from app.settings.config import settings

log = logging.getLogger(settings.APP_NAME)


async def authentication(access_token: Annotated[str, Header()]) -> User:
    try:
        email = await get_access_token_cache(access_token)
        return await get_user_if_exist(email)
    except (TokenNotExist, UserNotExist):
        log.error(f"Unauthorized Token error. {access_token}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized. Token error."
        )
