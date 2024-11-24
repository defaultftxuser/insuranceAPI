from dataclasses import dataclass
from typing import Any, Sequence

from sqlalchemy import select, insert, update, delete, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.repository.base import BaseSQLRepository


@dataclass(eq=False)
class InsuranceRepository(BaseSQLRepository):

    async def read(
        self,
        session: AsyncSession,
        data: dict[Any, Any],
        offset: int = 0,
        limit: int = 10,
    ) -> Sequence[RowMapping] | None:
        query = (
            select(self.model)
            .filter_by(**data)
            .offset(offset=offset)
            .limit(limit=limit)
        )
        result = await session.execute(query)
        return result.mappings().fetchall()

    async def create(self, session: AsyncSession, data: dict[Any, Any]) -> dict[Any, Any] | None:
        query = insert(self.model).values(**data).returning(self.model)
        result = await session.execute(query)
        return result.mappings().fetchone()

    async def update(
        self, session: AsyncSession, data: dict[Any, Any], change_data: dict[Any, Any]
    ) -> dict[Any, Any] | None:
        query = update(self.model).filter_by(**data).values(**change_data)
        result = await session.execute(query)
        return result.mappings().fetchone()

    async def delete(self, session: AsyncSession, data: dict[Any, Any]) -> dict[Any, Any] | None:
        query = delete(self.model).filter_by(**data).returning(self.model)
        result = await session.execute(query)
        return result.mappings().fetchone()
