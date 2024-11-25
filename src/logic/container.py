from functools import lru_cache
from uuid import uuid4

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from punq import Container, Scope

from src.common.settings.settings import ProjectSettings
from src.infra.db.db import PostgresClient, AsyncPostgresClient
from src.infra.message_broker.base import BaseMessageBroker
from src.infra.message_broker.kafka import KafkaMessageBroker
from src.infra.models.insurance_models import TariffModel
from src.infra.repository.insurance_repository import (
    BaseTariffRepository,
    TariffRepository,
)
from src.logic.comands.commands import (
    CreateTariffCommand,
    UpdateTariffCommand,
    DeleteTariffCommand,
    CreateTariffCommandHandler,
    UpdateTariffCommandHandler,
    DeleteTariffCommandHandler,
)
from src.logic.events.events import (
    TariffCreatedEventHandler,
    TariffUpdatedEventHandler,
    TariffDeletedEventHandler,
    TariffCreatedEvent,
    TariffUpdatedEvent,
    TariffDeletedEvent,
)
from src.logic.mediator.base import Mediator
from src.logic.other.user_service import dummy_price_service
from src.logic.query.queries import (
    GetTariffQueryHandler,
    TariffQuery,
    GetInsuranceQueryHandler, InsuranceQuery,
)


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    # common

    container.register(
        ProjectSettings, instance=ProjectSettings(), scope=Scope.singleton
    )

    settings: ProjectSettings = container.resolve(ProjectSettings)

    container.register(
        PostgresClient,
        factory=lambda: AsyncPostgresClient(settings=settings),
        scope=Scope.transient,
    )

    # infra

    client: AsyncPostgresClient = container.resolve(PostgresClient)

    container.register(
        BaseMessageBroker,
        instance=KafkaMessageBroker(
            consumer=AIOKafkaConsumer(
                bootstrap_servers=settings.bootstrap_server_kafka,
                group_id=f"chats-{uuid4()}",
                metadata_max_age_ms=30000,
            ),
            producer=AIOKafkaProducer(
                bootstrap_servers=settings.bootstrap_server_kafka,
            ),
        ),
        scope=Scope.singleton,
    )

    message_broker: KafkaMessageBroker = container.resolve(BaseMessageBroker)

    def init_insurance_repository() -> BaseTariffRepository:
        return TariffRepository(model=TariffModel)

    container.register(
        BaseTariffRepository,
        factory=init_insurance_repository,
        scope=Scope.singleton,
    )
    insurance_repository = container.resolve(BaseTariffRepository)

    # dummy services

    def init_mediator() -> Mediator:
        mediator = Mediator()

        # command handlers
        create_insurance_command_handler = CreateTariffCommandHandler(
            _event_mediator=mediator,
            insurance_repository=insurance_repository,
            client=client,
        )
        update_insurance_command_handler = UpdateTariffCommandHandler(
            _event_mediator=mediator,
            insurance_repository=insurance_repository,
            client=client,
        )
        delete_insurance_command_handler = DeleteTariffCommandHandler(
            _event_mediator=mediator,
            insurance_repository=insurance_repository,
            client=client,
        )
        # event handlers
        entity_created_handler = TariffCreatedEventHandler(
            message_broker=message_broker, broker_topic=settings.log_topic
        )
        entity_updated_handler = TariffUpdatedEventHandler(
            message_broker=message_broker, broker_topic=settings.log_topic
        )
        entity_deleted_handler = TariffDeletedEventHandler(
            message_broker=message_broker, broker_topic=settings.log_topic
        )
        # query handlers
        get_tariff_query_handler = GetTariffQueryHandler(
            insurance_repository=insurance_repository,
            client=client,
        )

        get_insurance_query_handler = GetInsuranceQueryHandler(
            insurance_repository=insurance_repository,
            client=client,
            price_calculator=dummy_price_service,
        )

        # register commands
        mediator.register_command(
            command=CreateTariffCommand,
            command_handlers=[create_insurance_command_handler],
        )
        mediator.register_command(
            command=UpdateTariffCommand,
            command_handlers=[update_insurance_command_handler],
        )
        mediator.register_command(
            command=DeleteTariffCommand,
            command_handlers=[delete_insurance_command_handler],
        )
        # register events
        mediator.register_event(
            event=TariffCreatedEvent, event_handlers=[entity_created_handler]
        )
        mediator.register_event(
            event=TariffUpdatedEvent, event_handlers=[entity_updated_handler]
        )
        mediator.register_event(
            event=TariffDeletedEvent, event_handlers=[entity_deleted_handler]
        )
        # register queries
        mediator.register_query(
            query=TariffQuery, query_handler=get_tariff_query_handler
        )
        mediator.register_query(
            query=InsuranceQuery, query_handler=get_insurance_query_handler
        )
        return mediator

    container.register(Mediator, factory=init_mediator, scope=Scope.singleton)

    return container
