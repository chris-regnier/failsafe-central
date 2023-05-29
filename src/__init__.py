from fastapi import FastAPI

from .api.reference import ReferenceRouter
from .api.process import ProcessRouter
from .api.projects import ProjectsRouter


def get_app(app: FastAPI = None) -> FastAPI:
    """
    FastAPI application factory.
    """
    if app is None:
        app = FastAPI()
    for router in [
        ReferenceRouter,
        ProjectsRouter,
        ProcessRouter,
    ]:
        app.include_router(router)
    return app
