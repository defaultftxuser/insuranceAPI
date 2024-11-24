from abc import abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Type

from src.logic.comands.base import BaseCommand, BaseCommandHandler, CR, CT


@dataclass(eq=False)
class BaseCommandMediator:
    commands_map: dict[BaseCommand, list[BaseCommandHandler]] = field(
        default_factory=lambda: defaultdict(list), kw_only=True
    )

    @abstractmethod
    async def handle_command(self, command: Type[CT]) -> CR:
        ...

    @abstractmethod
    async def register_command(
        self, command: Type[CT], command_handlers: list[BaseCommandHandler]
    ): ...
