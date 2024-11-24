from dataclasses import dataclass
from datetime import date

from src.domain.entitites.base import BaseEntity


@dataclass(eq=False)
class InsuranceEntityIn(BaseEntity):
    date: date
    cargo_type: str
    rate: float

    def validate(self):
        ...

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

    def validate(self):
        ...

    def to_dict(self):
        return {
            "date": self.date,
            "cargo_type": self.cargo_type,
            "rate": self.rate,
            "price": self.price,
        }
