from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from dataclasses import dataclass

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
    def get_engine(self): ...

    @abstractmethod
    def create_session(self): ...


@dataclass(eq=False)
class AsyncPostgresClient(PostgresClient):

    def get_engine(self) -> AsyncEngine:
        engine = create_async_engine(self.settings.get_sql_url())
        yield engine
        engine.dispose()

    @asynccontextmanager
    async def create_session(self) -> AsyncSession:
        session = async_sessionmaker(bind=self.get_engine(), class_=AsyncSession)
        try:
            yield session
            await session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
