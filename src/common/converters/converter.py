from dataclasses import asdict
from typing import Any

import orjson
from sqlalchemy import RowMapping

from src.domain.entitites.insurance_entities import InsuranceEntityWithPrice
from src.logic.events.base import BaseEvent


def convert_to_int(number: float) -> tuple[int, Any]:

    rate = 10 ** len(str(number).split(".")[-1])
    return rate, round(number * rate)


def convert_event_to_broker_message(event: BaseEvent) -> bytes:
    return orjson.dumps(event)


def convert_to_dict(event: BaseEvent) -> dict[str, Any]:
    return asdict(event)


def convert_from_model_to_entity(data_model: RowMapping[Any, Any]):
    return InsuranceEntityWithPrice(**data_model)
