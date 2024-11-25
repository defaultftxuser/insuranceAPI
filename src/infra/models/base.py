from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, UUID, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AbstractModel(Base):

    __abstract__ = True

    id = Column(UUID, default=uuid4, primary_key=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)