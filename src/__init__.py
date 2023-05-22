from fastapi import FastAPI

from .api import CollectionsAPIRouter
from .models.process import Cause, Effect, Failure
from .models.projects import Project, Role, Team, User
from .models.reference import Detection, Impact, Likelihood, Severity

App = FastAPI()
routers = [
    CollectionsAPIRouter(
        [Severity, Likelihood, Detection, Impact],
        prefix="/reference",
        tags=["reference"],
    ),
    CollectionsAPIRouter([Team, Project, User, Role], prefix="/projects"),
    CollectionsAPIRouter([Failure, Cause, Effect], prefix="/processes"),
]

for router in routers:
    App.include_router(router)
