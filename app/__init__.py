from fastapi import FastAPI
from app.config import settings


def create_app() -> FastAPI:
    app = FastAPI()

    from app.log import configure_logging

    configure_logging()

    # do this before loading routes
    from app.celery_app.celery_utils import create_celery

    app.celery_app = create_celery()

    from app.views import api_router

    app.include_router(api_router)

    @app.get("/")
    async def root():
        return {"message": f"API {settings.VERSION}"}

    return app
