from dataclasses import dataclass
from datetime import date
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.common.converters.converter import convert_from_model_to_entity
from src.infra.repository.insurance_repository import InsuranceRepository
from src.logic.query.base import BaseQuery, BaseQueryHandler, QR


@dataclass(eq=False)
class InsuranceEntityQuery(BaseQuery):
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
class GetInsuranceQueryHandler(BaseQueryHandler):
    insurance_repository: InsuranceRepository
    session: AsyncSession

    async def handle(self, query: InsuranceEntityQuery) -> QR:
        insurances = await self.insurance_repository.read(
            session=self.session,
            data=query.to_dict(),
            offset=query.offset,
            limit=query.limit,
        )
        if insurances:
            return [convert_from_model_to_entity(insurance) for insurance in insurances]
