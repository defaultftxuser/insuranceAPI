from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type, Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.common.filters.filters import PaginationFilters
from src.infra.models.base import BaseModel


@dataclass(eq=False)
class BaseSQLRepository(ABC):
    model: Type[BaseModel]

    @abstractmethod
    async def read(self, session: AsyncSession, data: dict[Any, Any], pagination_filters: PaginationFilters): ...

    @abstractmethod
    async def create(self, session: AsyncSession, data: dict[Any, Any]): ...

    @abstractmethod
    async def update(self, session: AsyncSession, data: dict[Any, Any], change_data: dict[Any, Any]): ...

    @abstractmethod
    async def delete(self, session: AsyncSession, data: dict[Any, Any]): ...
