from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

from src.common.converters.converter import convert_to_int
from src.domain.entitites.base import (
    BaseEntity,
)


@dataclass(eq=False)
class InsuranceEntityIn(BaseEntity):
    date: date
    cargo_type: str
    rate: float

    def validate(self): ...

    def convert_to_int_rate(self):
        rate, rate_convert = convert_to_int(self.rate)
        return {
            "date": self.date,
            "cargo_type": self.cargo_type,
            "rate": rate_convert,
            "divide_rate_convert": rate,
        }

    def to_dict(self):
        return {
            "date": self.date,
            "cargo_type": self.cargo_type,
            "rate": self.rate,
        }


@dataclass(eq=False)
class InsuranceEntityWithPrice(BaseEntity):
    date: date
    cargo_type: str
    rate: float | int
    price: float | int

    def validate(self): ...

    def to_dict(self):
        return {
            "date": self.date,
            "cargo_type": self.cargo_type,
            "rate": self.rate,
            "price": self.price,
        }


@dataclass(eq=False)
class InsuranceEntityWithPrice(BaseEntity):
    date: date
    cargo_type: str
    rate: float | int
    divide_rate_convert: float | int

    def validate(self): ...

    def to_dict(self):
        return {
            "date": self.date,
            "cargo_type": self.cargo_type,
            "rate": self.rate,
            "divide_rate_convert": self.divide_rate_convert,
        }


@dataclass(eq=False)
class InsuranceEntityWithPrice(BaseEntity):
    date: date
    cargo_type: str
    rate: int
    divide_rate_convert: int
    created_at: datetime
    updated_at: datetime

    def validate(self): ...

    def to_dict(self):
        return {
            "date": self.date,
            "cargo_type": self.cargo_type,
            "rate": self.rate,
            "divide_rate_convert": self.divide_rate_convert,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
