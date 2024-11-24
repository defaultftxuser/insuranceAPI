from dataclasses import dataclass

from datetime import date
from typing import Optional

from src.common.converters.converter import convert_event_to_broker_message
from src.domain.entitites.base import Operation, Status
from src.logic.events.base import BaseEvent, BaseEventHandler


@dataclass(eq=False)
class EntityCreatedEvent(BaseEvent):
    date: date
    cargo_type: str
    rate: float
    operation: Operation
    status: Status


@dataclass(eq=False)
class EntityFindEvent(BaseEvent):
    operation: Operation
    status: Status
    cargo_type: str | None = None
    rate: float | None = None
    date: Optional[date] = None


@dataclass(eq=False)
class EntityUpdateEvent(BaseEvent):
    date: date
    cargo_type: str
    rate: float
    operation: Operation
    status: Status


@dataclass(eq=False)
class EntityDeleteEvent(BaseEvent):
    date: date
    cargo_type: str
    rate: float
    operation: Operation
    status: Status


@dataclass(eq=False)
class EntityCreatedEventHandler(BaseEventHandler):
    async def handle(self, event: EntityCreatedEvent):
        await self.message_broker.send_message(
            key=str(event.event_id),
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
        )
