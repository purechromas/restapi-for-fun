import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.repositories.permission import add_tables_permissions_names
from app.repositories.role import add_system_roles
from app.settings.config import settings
from app.settings.logger_setup import config_logger
from app.settings.postgres import pg_helper, base_model

log = logging.getLogger(settings.APP_NAME)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управляет жизненным циклом приложения, включая создание таблиц в базе данных,
    добавление системных ролей и разрешений, настройку логирования, и т.д.
    """
    await pg_helper.create_tables(base_model)
    await add_system_roles()
    await add_tables_permissions_names()
    config_logger(settings.APP_NAME)
    log.info("[APP STACK] PostgresDB, Redis, SQLAlchemy, Pydentic, FastAPI, Uvicorn")
    yield
