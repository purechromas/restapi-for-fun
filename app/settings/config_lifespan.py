import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infra.postgres import pg_helper, base_model
from app.repositories.permission import add_tables_permissions_names
from app.repositories.role import add_system_roles
from app.settings.config_app import settings
from app.settings.config_logger import config_logger

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
    log.info("Application started and it was properly configuration")
    yield
    log.info("Postgres engine was disposed correctly")
    await pg_helper.dispose_engine()
