from dataclasses import dataclass

from datetime import date
from uuid import UUID

from src.common.converters.converter import convert_event_to_broker_message
from src.domain.entitites.base import Operation, Status
from src.logic.events.base import BaseEvent, BaseEventHandler


@dataclass(eq=False)
class EntityCreatedEvent(BaseEvent):
    user_id : UUID
    date: date
    cargo_type: str
    rate: float
    operation: Operation
    status: Status


@dataclass(eq=False)
class EntityUpdatedEvent(BaseEvent):
    user_id : UUID
    date: date
    cargo_type: str
    rate: float
    operation: Operation
    status: Status


@dataclass(eq=False)
class EntityDeletedEvent(BaseEvent):
    user_id : UUID
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


@dataclass(eq=False)
class EntityUpdatedEventHandler(BaseEventHandler):
    async def handle(self, event: EntityUpdatedEvent):
        await self.message_broker.send_message(
            key=str(event.event_id),
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
        )


@dataclass(eq=False)
class EntityDeletedEventHandler(BaseEventHandler):
    async def handle(self, event: EntityDeletedEvent):
        await self.message_broker.send_message(
            key=str(event.event_id),
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
        )
