from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable

from src.logic.comands.base import BaseCommand, BaseCommandHandler, CT
from src.logic.events.base import ET, ER, BaseEventHandler
from src.logic.mediator.command import BaseCommandMediator
from src.logic.mediator.event import BaseEventMediator
from src.logic.mediator.query import BaseQueryMediator
from src.logic.query.base import QT, QR, BaseQueryHandler


@dataclass(eq=False)
class Mediator(BaseCommandMediator, BaseEventMediator, BaseQueryMediator):
    events_map: dict[ET, list[BaseEventHandler]] = field(
        default_factory=lambda: defaultdict(list), kw_only=True
    )
    commands_map: dict[CT, list[BaseEventHandler]] = field(
        default_factory=lambda: defaultdict(list), kw_only=True
    )
    queries_map: dict[QT, BaseEventHandler] = field(
        default_factory=lambda: defaultdict, kw_only=True
    )

    async def register_command(
        self, command: BaseCommand, command_handlers: list[BaseCommandHandler]
    ):
        self.commands_map[command].extend(command_handlers)

    async def register_event(self, event: ET, event_handlers: list[BaseEventHandler]):
        self.events_map[event].extend(event_handlers)

    async def register_query(self, query: QT, query_handler: BaseQueryHandler):
        self.queries_map[query].append(query_handler)

    async def handle_command(self, command: BaseCommand):
        command_type = command.__class__
        handlers = self.commands_map[command_type]
        if not handlers:
            raise
        return [await handler.handle(command) for handler in handlers]

    async def publish(self, events: Iterable[ET]) -> ER:
        result = []
        for event in events:
            handlers: Iterable[BaseEventHandler] = self.events_map[event.__class__]
            result.extend([await handler.handle(event) for handler in handlers])
        return result

    async def handle_query(self, query: QT) -> QR:
        return self.queries_map[query.__class__].handle(query)
