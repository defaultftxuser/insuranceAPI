from datetime import date

from fastapi import APIRouter, Query, Depends
from punq import Container

from src.domain.entitites.tariff_entities import TariffEntityInWithoutRate
from src.logic.container import init_container
from src.logic.mediator.base import Mediator
from src.logic.query.queries import TariffQuery, InsuranceQuery

router = APIRouter(prefix="/api", tags=["insurance"])


@router.get("/insurance/")
async def get_insurance(
    date: date = Query(example="2024-01-01"),
    cargo_type: str = Query(example="Electronics"),
    container: Container = Depends(init_container),
):
    mediator: Mediator = container.resolve(Mediator)
    return await mediator.handle_query(
        InsuranceQuery(
            query_entity=TariffEntityInWithoutRate(date=date, cargo_type=cargo_type)
        )
    )
