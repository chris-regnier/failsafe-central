from fastapi import FastAPI

from .api.reference import ReferenceRouter
from .api.process import ProcessRouter
from .api.projects import ProjectsRouter

App = FastAPI()
routers = [
    ReferenceRouter,
    ProjectsRouter,
    ProcessRouter,
]

for router in routers:
    App.include_router(router)
