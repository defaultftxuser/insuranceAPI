from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field

from src.logic.query.base import QT, BaseQueryHandler, QR


@dataclass(eq=False)
class BaseQueryMediator(ABC):
    queries_map: dict[QT, BaseQueryHandler] = field(
        default_factory=lambda: defaultdict(list), kw_only=True
    )

    @abstractmethod
    async def handle_query(self, query: QT) -> QR: ...

    @abstractmethod
    async def register_query(
        self, query: QT, query_handler: BaseQueryHandler
    ): ...
