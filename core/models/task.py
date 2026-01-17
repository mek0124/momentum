from sqlalchemy import (
    Column, Integer, String,
    Boolean, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database.db import get_base


Base = get_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(
        Integer,
        primary_key = True,
        index = True,
        autoincrement = True
    )

    title = Column(
        String,
        unique = True,
        index = True
    )

    content = Column(String)

    completed = Column(
        Boolean,
        index = True,
        default = False
    )

    created_at = Column(
        DateTime,
        index = True,
        default = lambda: datetime.now()
    )
    
    user_id = Column(
        String,
        ForeignKey('users.id'),
        nullable=False
    )
    
    user = relationship("User", back_populates="tasks")