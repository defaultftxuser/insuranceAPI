from dataclasses import dataclass
from typing import Optional, Generic
from uuid import UUID

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.domain.entitites.base import Status, Operation
from src.domain.entitites.tariff_entities import (
    TariffEntityWithConvertRate,
    TariffEntityInWithoutRate,
    BaseTariffEntityQuery,
    BaseTariffEntityWithIdQuery,
)
from src.infra.db.db import AsyncPostgresClient
from src.infra.repository.insurance_repository import TariffRepository
from src.logic.comands.base import BaseCommand, BaseCommandHandler, CR, CT
from src.logic.events.events import (
    TariffCreatedEvent,
    TariffUpdatedEvent,
    TariffDeletedEvent,
)


@dataclass(eq=False)
class CreateTariffCommand(BaseCommand, Generic[CT, CR]):
    insurance_entity: TariffEntityWithConvertRate
    user_id: Optional[UUID] = None


@dataclass(eq=False)
class UpdateTariffCommand(BaseCommand):
    entity_to_update: BaseTariffEntityQuery
    change_entity: TariffEntityWithConvertRate
    user_id: Optional[UUID] = None


@dataclass(eq=False)
class DeleteTariffCommand(BaseCommand):
    insurance_entity: TariffEntityInWithoutRate
    user_id: Optional[UUID] = None


@dataclass(eq=False)
class UpdateTariffCommandHandler(BaseCommandHandler[CreateTariffCommand, CR]):
    insurance_repository: TariffRepository
    client: AsyncPostgresClient

    async def handle(self, command: UpdateTariffCommand) -> CR:
        async with self.client.create_session() as session:
            entity_event = command.entity_to_update
            try:
                model_result = await self.insurance_repository.update(
                    session=session,
                    data=command.entity_to_update.to_dict(),
                    change_data=command.change_entity.to_dict(),
                )
                await session.commit()
                entity_event.register_event(
                    TariffUpdatedEvent(
                        user_id=command.user_id,
                        status=Status.SUCCESS,
                        operation=Operation.UPDATED,
                        cargo_type=entity_event.cargo_type,
                        date=entity_event.date,
                        event_title="update",
                    )
                )
                await self._event_mediator.publish(events=entity_event.pull_events())
                return model_result
            except IntegrityError:
                entity_event.register_event(
                    TariffUpdatedEvent(
                        user_id=command.user_id,
                        status=Status.FAIL,
                        operation=Operation.UPDATED,
                        cargo_type=entity_event.cargo_type,
                        date=entity_event.date,
                        event_title="update",
                    )
                )
                return await self._event_mediator.publish(
                    events=entity_event.pull_events()
                )


@dataclass(eq=False)
class CreateTariffCommandHandler(BaseCommandHandler[CreateTariffCommand, CR]):
    insurance_repository: TariffRepository
    client: AsyncPostgresClient

    async def handle(self, command: CreateTariffCommand) -> CR:
        async with self.client.create_session() as session:
            entity_event = command.insurance_entity
            try:
                model_result = await self.insurance_repository.create(
                    session=session, data=command.insurance_entity.to_dict()
                )
                await session.commit()
                entity_event.register_event(
                    TariffCreatedEvent(
                        user_id=command.user_id,
                        status=Status.SUCCESS,
                        operation=Operation.CREATED,
                        cargo_type=entity_event.cargo_type,
                        rate=entity_event.divide_rate_convert / entity_event.rate,
                        date=entity_event.date,
                        event_title="creation",
                    )
                )
                await self._event_mediator.publish(events=entity_event.pull_events())
                return model_result
            except SQLAlchemyError:
                entity_event.register_event(
                    TariffCreatedEvent(
                        user_id=command.user_id,
                        status=Status.FAIL,
                        operation=Operation.CREATED,
                        cargo_type=entity_event.cargo_type,
                        rate=entity_event.divide_rate_convert / entity_event.rate,
                        date=entity_event.date,
                        event_title="creation",
                    )
                )
                await self._event_mediator.publish(events=entity_event.pull_events())
                raise SQLAlchemyError


@dataclass(eq=False)
class DeleteTariffCommandHandler(BaseCommandHandler[CreateTariffCommand, CR]):
    insurance_repository: TariffRepository
    client: AsyncPostgresClient

    async def handle(self, command: DeleteTariffCommand) -> CR:
        async with self.client.create_session() as session:
            entity_event = command.insurance_entity
            try:
                result_model = await self.insurance_repository.delete(
                    session=session, data=command.insurance_entity.to_dict()
                )
                await session.commit()
                if result_model:
                    entity_event.register_event(
                        TariffDeletedEvent(
                            user_id=command.user_id,
                            status=Status.SUCCESS,
                            operation=Operation.DELETED,
                            cargo_type=entity_event.cargo_type,
                            date=entity_event.date,
                            event_title="delete",
                        )
                    )
                    await self._event_mediator.publish(
                        events=entity_event.pull_events()
                    )
                    return result_model
                entity_event.register_event(
                    TariffDeletedEvent(
                        user_id=command.user_id,
                        status=Status.FAIL,
                        operation=Operation.DELETED,
                        cargo_type=entity_event.cargo_type,
                        date=entity_event.date,
                        event_title="delete",
                    )
                )
                await self._event_mediator.publish(events=entity_event.pull_events())
                return result_model
            except IntegrityError:
                entity_event.register_event(
                    TariffDeletedEvent(
                        user_id=command.user_id,
                        status=Status.FAIL,
                        operation=Operation.DELETED,
                        cargo_type=entity_event.cargo_type,
                        date=entity_event.date,
                        event_title="delete",
                    )
                )
                await self._event_mediator.publish(
                    events=entity_event.pull_events()
                )
                raise IntegrityError
