from pathlib import Path
from datetime import datetime

import pytz
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # БЕЗ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ 🔴
    APP_NAME: str = "victory_group"
    APP_VERSION: str = "0.1.0"
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    TIME_MOSCOW_NOW: datetime = datetime.now(pytz.timezone('Europe/Moscow'))

    # С ПЕРЕМЕННЫМИ ОКРУЖЕНИЯ ✅
    APP_SECRET_KEY: str = Field("asd123")
    APP_HOST: str = Field("localhost")
    APP_PORT: int = Field(8000)
    DEBUG: bool = Field(True, description="Включает также вывод логирование")
    SQLALCHEMY_ECHO: bool = Field(False, description="Включает вывод sqlalchemy echo")
    # Настройки JWT токена
    JWT_SECRET_KEY: str = Field("qwe123")
    JWT_ALGORITHM: str = Field("HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(120)
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(1440)
    # Настройки POSTGRES DB
    PG_URL: str = Field("postgresql+asyncpg://qwe123:qwe123@localhost:5432/postgres")
    PG_POOL: int = Field(
        50, description="Максимальное количество одновременно открытых соединений"
    )
    PG_POOL_TIMEOUT: int = Field(30, description="Таймаут запроса")
    # Настройки REDIS DB
    REDIS_URL: str = Field("redis://localhost:6379")
    REDIS_POOL: int = Field(
        20, description="Максимальное количество одновременно открытых соединений"
    )
    REDIS_POOL_TIMEOUT: int = Field(30, description="Таймаут запроса")

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
