from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, UUID, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):

    __abstract__ = True

    id = Column(UUID, default=uuid4, primary_key=True)
    created_at = Column(Date, default=datetime.now)
    updated_at = Column(Date, default=datetime.now, onupdate=datetime.now)