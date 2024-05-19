import logging

from fastapi import HTTPException, status

from app.cache.cache_tokens import set_access_token_cache
from app.api_v1.auth.schemas import (
    UserLoginOut,
    GetAccessTokenOut,
    UserRegistrationOut
)
from app.api_v1.auth.utils import (
    check_passwords_match,
    hash_password,
    check_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.settings.config import settings
from app.exceptions import UserNotExist, UserAlreadyExist
from app.models import User
from app.models.role import UserRoles
from app.repositories.user import create_user_if_not_exist, get_user_if_exist

log = logging.getLogger(settings.APP_NAME)


async def process_registration_request(user_data: dict) -> UserRegistrationOut:
    """
     Обрабатывает запрос на регистрацию пользователя.

     Параметры:
     - user_data (dict): Данные пользователя для регистрации.

     Возвращает:
     - UserRegistrationOut: Ответ с информацией о зарегистрированном пользователе.

     Исключения:
     - HTTPException: Если пользователь с таким email уже существует.
     """
    check_passwords_match(user_data["password"], user_data["confirm_password"])
    user_data["password"] = hash_password(user_data["password"])
    user_data["role_name"] = UserRoles(user_data["role_name"]).name
    try:
        user: User = await create_user_if_not_exist(user_data)
    except UserAlreadyExist:
        # We can take IP here and make sure that from one IP we have alot of registrations.
        log.error(
            f"User already exist: email: {user_data['email']} password:{user_data['password']}"
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with that kind of email already exists, try with another."
        )
    return UserRegistrationOut(email=user.email, role_name=user.role_name)


async def process_login_request(request_data: dict) -> UserLoginOut:
    """
       Обрабатывает запрос на аутентификацию пользователя.

       Параметры:
       - request_data (dict): Данные запроса на аутентификацию.

       Возвращает:
       - UserLoginOut: Ответ с токенами доступа.

       Исключения:
       - HTTPException: Если пользователь с таким email не существует или пароль неверный.
       """
    try:
        user: User = await get_user_if_exist(request_data["email"])
    except UserNotExist:
        # We can take IP here and make sure that we don't have security attacks.
        log.error(
            f"User not exist: email: {request_data['email']} password:{request_data['password']}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with that kind of email doesn't exist, try again."
        )

    check_password(request_data["password"], user.password)
    access_token = create_access_token(user.email)
    refresh_token = create_refresh_token(user.email)

    await set_access_token_cache(
        access_token,
        user.email,
        expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    return UserLoginOut(
        access_token=access_token,
        refresh_token=refresh_token
    )


async def process_access_token_request(request_data: dict) -> GetAccessTokenOut:
    """
    Обрабатывает запрос на обновление токена доступа.

    Параметры:
    - request_data (dict): Данные запроса на обновление токена.

    Возвращает:
    - GetAccessTokenOut: Ответ с новыми токенами доступа.

    Исключения:
    - HTTPException: Если токен обновления недействителен или пользователь
    с таким email не существует.
    """
    decoded_data: dict = decode_token(request_data["refresh_token"])

    try:
        user: User = await get_user_if_exist(decoded_data["email"])
    except UserNotExist:
        # We can take IP here and make sure that we don't have security attacks.
        log.error(f"UserNotExist: f{request_data['refresh_token']}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid token, user with that kind of token doesn't exist."
        )

    access_token = create_access_token(user.email)

    await set_access_token_cache(
        access_token,
        user.email,
        expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    return GetAccessTokenOut(
        access_token=access_token
    )
