"""accounts/models.py -- excerpt."""

import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from db import Base


class UserAccountStatus(str, enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DELETED = "deleted"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    status = Column(String, nullable=False, default=UserAccountStatus.ACTIVE.value)
    status_changed_at = Column(DateTime, nullable=True)
    status_changed_by = Column(String, nullable=True)  # admin user id or "system"
