from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Sequence

from sqlalchemy import select, insert, update, delete, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.filters.filters import PaginationFilters
from src.infra.repository.base import BaseSQLRepository


@dataclass(eq=False)
class BaseTariffRepository:
    @abstractmethod
    async def read_many(
        self,
        session: AsyncSession,
        data: dict[Any, Any],
        offset: int = 0,
        limit: int = 10,
    ): ...

    @abstractmethod
    async def read_one(
        self,
        session: AsyncSession,
        data: dict[Any, Any],
    ): ...

    @abstractmethod
    async def create(self, session: AsyncSession, data: dict[Any, Any]): ...

    @abstractmethod
    async def update(
        self, session: AsyncSession, data: dict[Any, Any], change_data: dict[Any, Any]
    ): ...

    @abstractmethod
    async def delete(self, session: AsyncSession, data: dict[Any, Any]): ...


@dataclass(eq=False)
class TariffRepository(BaseSQLRepository, BaseTariffRepository):
    async def read_one(
        self,
        session: AsyncSession,
        data: dict[Any, Any],
    ) -> Sequence[RowMapping] | None:
        query = select(
            self.model.date,
            self.model.cargo_type,
            self.model.rate,
            self.model.divide_rate_convert,
        ).filter_by(**data)
        result = await session.execute(query)
        return result.mappings().fetchone()

    async def read_many(
        self,
        session: AsyncSession,
        data: dict[Any, Any],
        limit: int = 10,
        offset: int = 0,
    ) -> Sequence[RowMapping] | None:
        query = (
            select(
                self.model.date,
                self.model.cargo_type,
                self.model.rate,
                self.model.divide_rate_convert,
            )
            .filter_by(**data)
            .offset(offset=offset)
            .limit(limit=limit)
        )
        result = await session.execute(query)
        return result.mappings().fetchall()

    async def create(
        self, session: AsyncSession, data: dict[Any, Any]
    ) -> dict[Any, Any] | None:
        query = (
            insert(self.model)
            .values(**data)
            .returning(
                self.model.date,
                self.model.cargo_type,
                self.model.rate,
                self.model.divide_rate_convert,
            )
        )
        result = await session.execute(query)
        return result.mappings().fetchone()

    async def update(
        self, session: AsyncSession, data: dict[Any, Any], change_data: dict[Any, Any]
    ) -> dict[Any, Any] | None:
        query = (
            update(self.model)
            .filter_by(**data)
            .values(**change_data)
            .returning(
                self.model.date,
                self.model.cargo_type,
                self.model.rate,
                self.model.divide_rate_convert,
            )
        )
        result = await session.execute(query)
        return result.mappings().fetchone()

    async def delete(
        self, session: AsyncSession, data: dict[Any, Any]
    ) -> dict[Any, Any] | None:
        query = (
            delete(self.model).filter_by(**data)
            .returning(
                self.model.__table__.columns,
            )
        )
        result = await session.execute(query)
        return result.mappings().fetchone()
