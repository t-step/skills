from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("postgresql+psycopg2://localhost/todolist")


def get_session() -> Session:
    return Session(engine)
