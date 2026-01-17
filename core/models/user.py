from sqlalchemy import (
    Column, String, DateTime
)
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4

from ..database.db import get_base


Base = get_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(
        String,
        primary_key = True,
        index = True,
        unique = True,
        default = lambda: str(uuid4())
    )

    username = Column(
        String,
        unique = True,
        index = True
    )

    created_at = Column(
        DateTime,
        index = True,
        default = lambda: datetime.now()
    )

    updated_at = Column(
        DateTime,
        index = True,
        default = lambda: datetime.now(),
        onupdate = lambda: datetime.now()
    )

    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")