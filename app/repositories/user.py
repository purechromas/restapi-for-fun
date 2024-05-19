from sqlalchemy import select

from app.exceptions import UserNotExist, UserAlreadyExist
from app.settings.postgres import get_async_session
from app.models import User


async def create_user_if_not_exist(user_data: dict) -> User:
    """
    Создает пользователя, если пользователь с указанным адресом электронной почты не существует.
    Если пользователь с таким адресом электронной почты уже существует,
    выбрасывает исключение UserAlreadyExist.
    """
    async for session in get_async_session():
        stmt = select(User).where(User.email == user_data["email"])
        result = await session.execute(stmt)

        if result.scalar_one_or_none():
            raise UserAlreadyExist

        user = User(
            email=user_data["email"],
            password=user_data["password"],
            role_name=user_data["role_name"]
        )

        session.add(user)
        await session.commit()

        await session.refresh(user)

        return user


async def get_user_if_exist(email: str) -> User:
    """
     Получает пользователя по адресу электронной почты.
     Если пользователь с таким адресом электронной почты не существует,
     выбрасывает исключение UserNotExist.
     """
    async for session in get_async_session():
        stmt = select(User).where(User.email == email)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise UserNotExist

        return user
