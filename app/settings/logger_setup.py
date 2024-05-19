import logging
import os
from logging.handlers import RotatingFileHandler

from app.settings.config import settings


def config_logger(logger_name: str):
    """
    Создает базовую конфигурацию логирования для вывода сообщений в консоль и файл.
    Файлы логов ротируются ежедневно, их размер ограничен 30 мегабайтами.
    Хранятся логи за последние 7 дней.
    """

    logger = logging.getLogger(logger_name)  # Create a new logger instance with the provided name
    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    console_out = logging.StreamHandler()
    rotate = RotatingFileHandler(
        filename=os.path.join(settings.BASE_DIR, f"logs/{settings.APP_NAME}.log"),
        maxBytes=30 * 1024 * 1024,  # 30 MB
        backupCount=7
    )

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s: %(message)s')
    console_out.setFormatter(formatter)
    rotate.setFormatter(formatter)

    logger.addHandler(rotate)
    logger.addHandler(console_out)
