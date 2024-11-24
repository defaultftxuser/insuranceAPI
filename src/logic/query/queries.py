from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from src.common.converters.converter import convert_from_model_to_entity
from src.domain.entitites.insurance_entities import InsuranceEntityQuery
from src.infra.repository.insurance_repository import InsuranceRepository
from src.logic.query.base import BaseQuery, BaseQueryHandler, QR


@dataclass(eq=False)
class InsuranceEntityQuery(BaseQuery):
    query_entity: InsuranceEntityQuery


@dataclass(eq=False)
class GetInsuranceQueryHandler(BaseQueryHandler):
    insurance_repository: InsuranceRepository
    session: AsyncSession

    async def handle(self, query: InsuranceEntityQuery) -> QR:
        insurances = await self.insurance_repository.read(
            session=self.session,
            data=query.query_entity.to_dict(),
            offset=query.query_entity.offset,
            limit=query.query_entity.limit,
        )
        if insurances:
            return [convert_from_model_to_entity(insurance) for insurance in insurances]
