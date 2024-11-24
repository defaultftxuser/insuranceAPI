from abc import abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field

from src.logic.comands.base import BaseCommand, BaseCommandHandler


@dataclass(eq=False)
class BaseCommandMediator:
    commands_map: dict[BaseCommand, list[BaseCommandHandler]] = field(
        default_factory=lambda: defaultdict(list), kw_only=True
    )

    @abstractmethod
    async def handle_command(self, command: BaseCommand): ...

    @abstractmethod
    async def register_command(
        self, command: BaseCommand, command_handlers: list[BaseCommandHandler]
    ): ...
