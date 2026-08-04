from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class TodoItem(Base):
    __tablename__ = "todo_items"

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(200), nullable=False)
    done: bool = Column(Boolean, default=False)
