from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Any


@dataclass(eq=False)
class BaseEvent(ABC): ...


ET = TypeVar("ET", bound=BaseEvent)
ER = TypeVar("ER", bound=Any)


@dataclass(eq=False)
class BaseEventHandler(ABC):
    @abstractmethod
    async def handle(self, event: ET) -> ER:
        ...