from fastapi import FastAPI

from .api.reference import ReferenceRouter
from .api.process import ProcessRouter
from .api.projects import ProjectsRouter


def get_app() -> FastAPI:
    """
    FastAPI application factory.
    """
    app = FastAPI()
    for router in [
        ReferenceRouter,
        ProjectsRouter,
        ProcessRouter,
    ]:
        app.include_router(router)
    return app
