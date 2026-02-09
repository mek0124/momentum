from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

from ..database.db import get_base


Base = get_base()


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, index = True, primary_key = True)
    title = Column(String, index = True, unique = True)
    details = Column(String)
    priority = Column(Integer, index = True, default = 3)
    created_at = Column(DateTime, index = True, default = lambda: datetime.now())
    updated_at = Column(DateTime, index = True, default = lambda: datetime.now(), onupdate = lambda: datetime.now())