from abc import ABC, abstractmethod
from copy import copy
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from src.logic.events.base import BaseEvent, ET


class Operation(Enum):
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"
    READED = "readed"


class Status(Enum):
    SUCCESS = "success"
    FAIL = "fail"


@dataclass(eq=False)
class BaseEntity(ABC):
    _events: list[BaseEvent] = field(default_factory=list, kw_only=True)
    created_at: datetime = field(default_factory=datetime.now, kw_only=True)

    def __post_init__(self):
        self.validate()

    @abstractmethod
    def validate(self): ...

    @abstractmethod
    def to_dict(self): ...

    def register_event(self, event: ET):
        self._events.append(event)

    def pull_events(self) -> list[ET]:
        registered_events = copy(self._events)
        self._events.clear()
        return registered_events
