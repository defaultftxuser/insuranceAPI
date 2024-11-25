from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable

from src.logic.comands.base import BaseCommand, BaseCommandHandler, CT, CR
from src.logic.events.base import ET, ER, BaseEventHandler, BaseEvent
from src.logic.mediator.command import BaseCommandMediator
from src.logic.mediator.event import BaseEventMediator
from src.logic.mediator.query import BaseQueryMediator
from src.logic.query.base import QT, QR, BaseQueryHandler, BaseQuery


@dataclass(eq=False)
class Mediator(BaseCommandMediator, BaseEventMediator, BaseQueryMediator):
    events_map: dict[ET, list[BaseEventHandler]] = field(
        default_factory=lambda: defaultdict(list), kw_only=True
    )
    commands_map: dict[CT, list[BaseCommandHandler]] = field(
        default_factory=lambda: defaultdict(list), kw_only=True
    )
    queries_map: dict[QT, list[BaseQueryHandler]] = field(  # Здесь исправлено
        default_factory=lambda: defaultdict(list), kw_only=True
    )

    def register_command(
        self,
        command: BaseCommand,
        command_handlers: Iterable[BaseCommandHandler[CT, CR]],
    ):
        self.commands_map[command].extend(command_handlers)

    def register_event(
        self, event: BaseEvent, event_handlers: Iterable[BaseEventHandler[ET, ER]]
    ):
        self.events_map[event].extend(event_handlers)

    def register_query(self, query: BaseQuery, query_handler: BaseQueryHandler):
        self.queries_map[query].append(query_handler)

    async def handle_command(self, command: BaseCommand):
        command_type = command.__class__
        handlers = self.commands_map[command_type]
        if not handlers:
            raise ValueError(f"No handlers found for command {command_type}")
        return [await handler.handle(command) for handler in handlers]

    async def publish(self, events: Iterable[ET]) -> ER:
        result = []
        for event in events:
            handlers: Iterable[BaseEventHandler] = self.events_map[event.__class__]
            result.extend([await handler.handle(event) for handler in handlers])
        return result

    async def handle_query(self, query: QT) -> QR:
        handlers = self.queries_map[query.__class__]
        if not handlers:
            raise ValueError(f"No handlers found for query {query.__class__}")
        if len(handlers) > 1:
            raise ValueError(f"Multiple handlers found for query {query.__class__}")
        return await handlers[0].handle(query)