from fastapi import FastAPI

from .api import CollectionsAPIRouter
from .models import Detection, Impact, Likelihood, Severity


App = FastAPI()


App.include_router(CollectionsAPIRouter([Severity, Likelihood, Detection, Impact]))
