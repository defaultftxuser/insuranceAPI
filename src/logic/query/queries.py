from dataclasses import dataclass

from src.domain.entitites.tariff_entities import (
    TariffEntityInWithoutRate,
    InsuranceEntityOut,
    TariffEntityOut,
)
from src.infra.db.db import AsyncPostgresClient
from src.infra.repository.insurance_repository import TariffRepository
from src.logic.other.user_service import dummy_price_service
from src.logic.query.base import BaseQuery, BaseQueryHandler, QR


@dataclass(eq=False)
class InsuranceQuery(BaseQuery):
    query_entity: TariffEntityInWithoutRate


@dataclass(eq=False)
class GetInsuranceQueryHandler(BaseQueryHandler):
    insurance_repository: TariffRepository
    client: AsyncPostgresClient
    price_calculator: dummy_price_service  # поменять на сервис расчета стоимости

    async def handle(self, query: InsuranceQuery) -> QR:
        async with self.client.create_session() as session:
            tariff = await self.insurance_repository.read_one(
                session=session,
                data=query.query_entity.to_dict(),
            )
            if tariff:

                return InsuranceEntityOut(
                    date=tariff.get("date"),
                    price=self.price_calculator()
                    * tariff.get("divide_rate_convert")
                    / tariff.get("rate"),
                    cargo_type=tariff.get("cargo_type"),
                )
            return


@dataclass(eq=False)
class TariffQuery(BaseQuery):
    query_entity: TariffEntityInWithoutRate


@dataclass(eq=False)
class GetTariffQueryHandler(BaseQueryHandler):
    insurance_repository: TariffRepository
    client: AsyncPostgresClient

    async def handle(self, query: TariffQuery) -> QR:
        async with self.client.create_session() as session:
            tariff = await self.insurance_repository.read_one(
                session=session,
                data=query.query_entity.to_dict(),
            )
            if tariff:

                return TariffEntityOut(
                    date=tariff.get("date"),
                    rate=tariff.get("divide_rate_convert") / tariff.get("rate"),
                    cargo_type=tariff.get("cargo_type"),
                )
            return
