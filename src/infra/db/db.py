from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
    AsyncEngine,
)

from src.common.settings.settings import ProjectSettings


@dataclass(eq=False)
class PostgresClient(ABC):
    settings: ProjectSettings

    @abstractmethod
    def create_session(self): ...


@dataclass(eq=False)
class AsyncPostgresClient(PostgresClient):
    def __post_init__(self):
        self.engine = create_async_engine(self.settings.get_sql_url)
        self.session_factory = async_sessionmaker(
            bind=self.engine, class_=AsyncSession
        )

    @asynccontextmanager
    async def create_session(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
