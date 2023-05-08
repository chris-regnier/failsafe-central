from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine

from src.api import CollectionsAPIRouter
from src.models import Detection, Impact, Likelihood, Severity


App = FastAPI()

engine = create_engine("sqlite:///db.sqlite3")

setup_db = lambda: SQLModel.metadata.create_all(engine)

App.add_middleware(setup_db)
App.include_router(CollectionsAPIRouter([Severity, Likelihood, Detection, Impact]))
