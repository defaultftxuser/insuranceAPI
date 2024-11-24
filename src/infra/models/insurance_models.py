from sqlalchemy import Column, Date, String, Integer, UniqueConstraint

from src.infra.models.base import BaseModel


class InsuranceModel(BaseModel):

    __tablename__ = "insurances"

    date = Column(Date, nullable=False)
    cargo_type = Column(String, nullable=False)
    rate = Column(Integer, nullable=False)
    divide_rate_convert = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint("cargo_type", "date", name="_cargo_type_date_uc"),
    )
