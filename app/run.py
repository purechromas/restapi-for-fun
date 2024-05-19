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
        debug=settings.DEBUG,
        lifespan=lifespan,
    )
    fast_api.include_router(auth_routers)
    fast_api.include_router(project_routers)
    return fast_api


if __name__ == "__main__":
    app = init_app()
    uvicorn.run(app=app, host=settings.APP_HOST, port=settings.APP_PORT)
