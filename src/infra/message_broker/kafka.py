from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from dataclasses import dataclass

import orjson

from src.infra.message_broker.base import BaseMessageBroker


@dataclass(eq=False)
class KafkaMessageBroker(BaseMessageBroker):
    consumer: AIOKafkaConsumer
    producer: AIOKafkaProducer

    async def start(self):
        await self.producer.start()
        await self.consumer.start()

    async def close(self):
        await self.producer.stop()
        await self.consumer.stop()

    async def send_message(self, topic: str, key: str, value: bytes):
        await self.producer.send(topic=topic, key=key.encode(), value=value)

    async def start_consuming(self, topic: str):
        self.consumer.subscribe(topics=[topic])
        async for message in self.consumer:
            yield orjson.loads(message.value)

    async def stop_consuming(self):
        await self.consumer.unsubscribe()
