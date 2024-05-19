import uvicorn
from fastapi import FastAPI
from app.api_v1.auth.endpoints import auth_routers
from app.api_v1.project.endpoints import project_routers
from app.settings.config import settings
from app.settings.lifespan import lifespan


def init_app() -> FastAPI:
    fast_api = FastAPI(
        title="Group Victory Test RestAPI",
        docs_url="/",
        lifespan=lifespan,
    )
    fast_api.include_router(auth_routers)
    fast_api.include_router(project_routers)
    return fast_api


if __name__ == "__main__":
    uvicorn.run(
        "run:init_app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG
    )
