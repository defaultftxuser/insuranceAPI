from sqlalchemy import Column, Date, String, Integer

from src.infra.models.base import BaseModel


class InsuranceModel(BaseModel):

    __tablename__ = "insurances"

    date = Column(Date, nullable=False)
    cargo_type = Column(String, nullable=False)
    rate = Column(Integer, nullable=False)
    rate_convert = Column(Integer, nullable=False)
