from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Any, Generic


@dataclass(eq=False)
class BaseQuery(ABC): ...


QT = TypeVar("QT", bound=BaseQuery)
QR = TypeVar("QR", bound=Any)


@dataclass(eq=False)
class BaseQueryHandler(ABC, Generic[QT, QR]):

    @abstractmethod
    async def handle(self, query: QT) -> QR: ...
