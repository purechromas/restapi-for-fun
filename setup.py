from setuptools import setup, find_packages

from app.settings.config_app import settings

setup(
    name=settings.APP_NAME,
    version=settings.APP_VERSION,
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "restapi = app.cmd.restapi:run_api"
        ],
    },
)
