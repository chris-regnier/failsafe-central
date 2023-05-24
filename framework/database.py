"""
Manages the database connections and interactions so that they can be imported
consistently across the application.
"""
import os
from sqlmodel import SQLModel, Session, create_engine

DB_URL = os.getenv("FAILSAFE_DB_URL", "sqlite:///db.sqlite3")


def get_db():
    connect_args = {}
    # Handle DB-specific connection args
    if DB_URL.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    engine = create_engine(DB_URL, connect_args=connect_args)
    try:
        SQLModel.metadata.create_all(engine, checkfirst=True)
    except:
        raise  # Database already exists
    try:
        with Session(engine, autoflush=True, autocommit=False) as session:
            yield session
    finally:
        session.close()
