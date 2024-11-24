from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import TypeVar, Any
from uuid import UUID, uuid4

from src.infra.message_broker.base import BaseMessageBroker


@dataclass(eq=False)
class BaseEvent(ABC):
    event_title: str
    occurred_at : datetime = field(default_factory=datetime.now, kw_only=True)
    event_id: UUID = field(default_factory=uuid4, kw_only=True)


ET = TypeVar("ET", bound=BaseEvent)
ER = TypeVar("ER", bound=Any)


@dataclass(eq=False)
class BaseEventHandler(ABC):
    message_broker: BaseMessageBroker
    broker_topic: str | None = None

    @abstractmethod
    async def handle(self, event: ET) -> ER: ...


