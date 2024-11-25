from dataclasses import dataclass

from datetime import date
from uuid import UUID

from src.domain.entitites.base import Operation, Status
from src.logic.events.base import BaseEvent, BaseEventHandler


@dataclass(eq=False)
class TariffCreatedEvent(BaseEvent):
    user_id : UUID
    date: date
    cargo_type: str
    rate: float
    operation: Operation
    status: Status


@dataclass(eq=False)
class TariffUpdatedEvent(BaseEvent):
    user_id : UUID
    date: date
    cargo_type: str
    operation: Operation
    status: Status


@dataclass(eq=False)
class TariffDeletedEvent(BaseEvent):
    user_id : UUID
    date: date
    cargo_type: str
    operation: Operation
    status: Status


@dataclass(eq=False)
class TariffCreatedEventHandler(BaseEventHandler):
    async def handle(self, event: TariffCreatedEvent):
        await self.message_broker.send_message(
            key=str(event.event_id),
            topic=self.broker_topic,
            value=event.convert_event_to_broker_message())


@dataclass(eq=False)
class TariffUpdatedEventHandler(BaseEventHandler):
    async def handle(self, event: TariffUpdatedEvent):
        await self.message_broker.send_message(
            key=str(event.event_id),
            topic=self.broker_topic,
            value=event.convert_event_to_broker_message())


@dataclass(eq=False)
class TariffDeletedEventHandler(BaseEventHandler):
    async def handle(self, event: TariffDeletedEvent):
        await self.message_broker.send_message(
            key=str(event.event_id),
            topic=self.broker_topic,
            value=event.convert_event_to_broker_message())
