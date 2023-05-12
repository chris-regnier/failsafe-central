"""
Manages the database connections and interactions so that they can be imported
consistently across the application.
"""
from sqlmodel import SQLModel, Session, create_engine


def get_db():
    engine = create_engine(
        "sqlite:///db.sqlite3", connect_args={"check_same_thread": False}
    )
    try:
        SQLModel.metadata.create_all(engine, checkfirst=True)
    except:
        raise  # Database already exists
    try:
        with Session(engine, autoflush=True, autocommit=False) as session:
            yield session
    finally:
        session.close()
