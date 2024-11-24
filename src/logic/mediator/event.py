from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field

from src.logic.events.base import BaseEventHandler, ET, ER


@dataclass(eq=False)
class BaseEventMediator(ABC):
    events_map: dict[ET, list[BaseEventHandler]] = field(
        default_factory=lambda: defaultdict(list), kw_only=True
    )

    @abstractmethod
    async def publish(self, events: list[ET]) -> ER: ...

    @abstractmethod
    async def register_event(
        self, event: ET, event_handlers: list[BaseEventHandler]
    ): ...
