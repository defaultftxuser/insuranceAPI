from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional
from uuid import UUID, uuid4

from src.common.converters.converter import convert_to_int
from src.domain.entitites.base import (
    BaseEntity,
)


@dataclass(eq=False)
class TariffEntityInWithoutRate(BaseEntity):
    date: date
    cargo_type: str

    def validate(self): ...

    def to_dict(self):
        return {
            "date": self.date,
            "cargo_type": self.cargo_type,
        }


@dataclass(eq=False)
class TariffEntityIn(TariffEntityInWithoutRate):
    rate: int

    def to_dict(self):
        return {
            "date": self.date,
            "cargo_type": self.cargo_type,
            "rate": self.rate,
        }


@dataclass(eq=False)
class TariffEntityWithConvertRate(TariffEntityIn):
    divide_rate_convert: int

    def to_dict(self):
        return {
            "date": self.date,
            "cargo_type": self.cargo_type,
            "rate": self.rate,
            "divide_rate_convert": self.divide_rate_convert,
        }


@dataclass(eq=False)
class BaseTariffEntityQuery(BaseEntity):
    date: Optional[date] = None
    cargo_type: str | None = None
    rate: float | int | None = None

    def validate(self): ...

    def to_dict(self):
        return {
            key: value
            for key, value in {
                "date": self.date,
                "cargo_type": self.cargo_type,
                "rate": self.rate,
            }.items()
            if value is not None
        }


@dataclass(eq=False)
class TariffWithPrice(BaseEntity):
    id: UUID
    date: date
    cargo_type: str
    rate: int
    divide_rate_convert: int
    created_at: datetime
    updated_at: datetime

    def validate(self): ...

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "cargo_type": self.cargo_type,
            "rate": self.rate,
            "divide_rate_convert": self.divide_rate_convert,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass(eq=False)
class BaseTariffEntityWithIdQuery(BaseTariffEntityQuery):
    id: UUID = None

    def validate(self): ...

    def to_dict(self):
        return {
            key: value
            for key, value in {
                "id": self.id,
                "date": self.date,
                "cargo_type": self.cargo_type,
                "rate": self.rate,
            }.items()
            if value is not None
        }


@dataclass(eq=False)
class TariffEntityQuery(BaseTariffEntityQuery):
    date: Optional[date] = None
    cargo_type: str | None = None
    rate: float | int | None = None
    limit: int = 10
    offset: int = 0

    def to_dict(self):
        return {
            key: value
            for key, value in {
                "date": self.date,
                "cargo_type": self.cargo_type,
                "rate": self.rate,
            }.items()
            if value is not None
        }


@dataclass(eq=False)
class DummyUserId:
    id: UUID = field(default_factory=uuid4)


@dataclass(eq=False)
class TariffEntityOut:
    date: date
    rate: float
    cargo_type: str


@dataclass(eq=False)
class InsuranceEntityOut:
    date: date
    price: float
    cargo_type: str
