from dataclasses import dataclass
from typing import Any

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.filters.filters import PaginationFilters
from src.infra.repository.base import BaseSQLRepository


@dataclass(eq=False)
class InsuranceRepository(BaseSQLRepository):

    async def read(self, session: AsyncSession, data: dict[Any, Any], pagination_filters: PaginationFilters) -> ...:
        query = select(self.model).filter_by(**data)
        result = await session.execute(query)
        return result.mappings().fetchall()

    async def create(self, session: AsyncSession, data: dict[Any, Any]) -> ...:
        query = insert(self.model).values(**data).returning(self.model)
        result = await session.execute(query)
        return result.mappings().fetchone()

    async def update(
        self, session: AsyncSession, data: dict[Any, Any], change_data: dict[Any, Any]
    ) -> ...:
        query = update(self.model).filter_by(**data).values(**change_data)
        result = await session.execute(query)
        return result.mappings().fetchone()

    async def delete(self, session: AsyncSession, data: dict[Any, Any]) -> ...:
        query = delete(self.model).filter_by(**data).returning(self.model)
        result = await session.execute(query)
        return result.mappings().fetchone()