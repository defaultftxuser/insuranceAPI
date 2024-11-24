from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Type, Any, Generic

from src.logic.mediator.event import BaseEventMediator


@dataclass(eq=False)
class BaseCommand(ABC): ...


CT = TypeVar("CT", bound=BaseCommand)
CR = TypeVar("CR", bound=Any)


@dataclass(eq=False)
class BaseCommandHandler(ABC, Generic[CT, CR]):
    _event_mediator: BaseEventMediator

    @abstractmethod
    async def handle(self, command: CT) -> CR: ...
