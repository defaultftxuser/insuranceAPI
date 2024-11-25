from datetime import date

from fastapi import APIRouter, Depends, Query, HTTPException
from punq import Container
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from src.domain.entitites.tariff_entities import (
    TariffEntityInWithoutRate,
    BaseTariffEntityQuery,
    TariffEntityWithConvertRate,
)
from src.domain.schemas.tariff_schemas import CargoRateSchema, TariffItem
from src.logic.comands.commands import (
    CreateTariffCommand,
    DeleteTariffCommand,
    UpdateTariffCommand,
)
from src.logic.container import init_container
from src.logic.mediator.base import Mediator
from src.logic.query.queries import TariffQuery

router = APIRouter(prefix="/api", tags=["tariff"])


@router.post("/tariff")
async def create_tariff(
    schema: CargoRateSchema, container: Container = Depends(init_container)
):
    mediator: Mediator = container.resolve(Mediator)
    list_of_tariffs = schema.to_entities()
    results = []
    for tariff in list_of_tariffs:
        try:
            results.append(
                await mediator.handle_command(
                    CreateTariffCommand(insurance_entity=tariff)
                )
            )
        except SQLAlchemyError:
            results.append(
                {
                    "data": f"{tariff.cargo_type=} wit that {tariff.date=} already exists, if u want to mutate it, go to patch method "
                }
            )
    return results


@router.delete("/tariff")
async def delete_tariff(
    date: date = Query(example="2024-01-01"),
    cargo_type: str = Query(example="Electronics"),
    container: Container = Depends(init_container),
):
    mediator: Mediator = container.resolve(Mediator)
    try:
        result = await mediator.handle_command(
            DeleteTariffCommand(
                insurance_entity=TariffEntityInWithoutRate(
                    date=date, cargo_type=cargo_type
                )
            )
        )
        if result:
            return result
        return HTTPException(status_code=404, detail="model not found")
    except IntegrityError:
        return HTTPException(status_code=404, detail="can't delete, this model")


@router.patch("/tariff")
async def mutate_tariff(
    schema: TariffItem,
    date: date = Query(example="2024-01-01"),
    cargo_type: str = Query(example="Electronics"),
    container: Container = Depends(init_container),
):
    mediator: Mediator = container.resolve(Mediator)
    try:
        result = await mediator.handle_command(
            UpdateTariffCommand(
                entity_to_update=BaseTariffEntityQuery(
                    date=date, cargo_type=cargo_type
                ),
                change_entity=TariffEntityWithConvertRate(
                    **schema.to_entities().to_dict()
                ),
            )
        )
        return result
    except SQLAlchemyError:
        raise HTTPException(status_code=404, detail="U can't mutate this model")


@router.get("/tariff/")
async def get_tariff(
    date: date = Query(example="2024-01-01"),
    cargo_type: str = Query(example="Electronics"),
    container: Container = Depends(init_container),
):
    mediator: Mediator = container.resolve(Mediator)
    return await mediator.handle_query(
        TariffQuery(
            query_entity=TariffEntityInWithoutRate(date=date, cargo_type=cargo_type)
        )
    )
