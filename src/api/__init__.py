from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine

App = FastAPI()

engine = create_engine("sqlite:///db.sqlite3")

setup_db = lambda: SQLModel.metadata.create_all(engine)

App.setup_db = setup_db