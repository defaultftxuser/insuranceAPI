from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import TypeVar, Any, Generic
from uuid import UUID, uuid4

from orjson import orjson

from src.infra.message_broker.base import BaseMessageBroker


@dataclass(eq=False)
class BaseEvent(ABC):
    event_title: str
    occurred_at: datetime = field(default_factory=datetime.now, kw_only=True)
    event_id: UUID = field(default_factory=uuid4, kw_only=True)

    def convert_event_to_broker_message(self) -> bytes:
        return orjson.dumps(self)

    def convert_to_dict(self) -> dict[str, Any]:
        return asdict(self)



ET = TypeVar("ET", bound=BaseEvent)
ER = TypeVar("ER", bound=Any)


@dataclass(eq=False)
class BaseEventHandler(ABC, Generic[ET, ER]):
    message_broker: BaseMessageBroker
    broker_topic: str | None = None

    @abstractmethod
    async def handle(self, event: ET) -> ER: ...
