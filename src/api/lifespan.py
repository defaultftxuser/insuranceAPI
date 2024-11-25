from punq import Container

from src.infra.db.db import AsyncPostgresClient, PostgresClient
from src.infra.message_broker.base import BaseMessageBroker
from src.infra.message_broker.kafka import KafkaMessageBroker
from src.infra.models.base import Base
from src.logic.container import init_container


async def start_broker():
    container: Container = init_container()
    message_broker: KafkaMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.start()


async def stop_broker():
    container: Container = init_container()
    message_broker: KafkaMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.close()


async def run_migrations():
    client: AsyncPostgresClient = init_container().resolve(PostgresClient)
    async with client.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
