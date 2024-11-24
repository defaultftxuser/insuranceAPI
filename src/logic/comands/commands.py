from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entitites.base import Status, Operation
from src.domain.entitites.insurance_entities import (
    InsuranceEntityIn,
    InsuranceEntityQuery,
)
from src.infra.repository.insurance_repository import InsuranceRepository
from src.logic.comands.base import BaseCommand, BaseCommandHandler, CR
from src.logic.events.events import (
    EntityCreatedEvent,
    EntityUpdatedEvent,
    EntityDeletedEvent,
)


@dataclass(eq=False)
class CreateInsuranceCommand(BaseCommand):
    insurance_entity: InsuranceEntityQuery
    user_id: Optional[UUID] = None


@dataclass(eq=False)
class UpdateInsuranceCommand(BaseCommand):
    entity_to_update: InsuranceEntityQuery
    insurance_id: UUID
    user_id: Optional[UUID] = None


@dataclass(eq=False)
class DeleteInsuranceCommand(BaseCommand):
    insurance_entity: InsuranceEntityIn
    user_id: Optional[UUID] = None


class UpdateInsuranceCommandHandler(BaseCommandHandler[CreateInsuranceCommand, CR]):
    insurance_repository: InsuranceRepository
    session: AsyncSession

    async def handle(self, command: CreateInsuranceCommand) -> CR:
        entity_event = command.insurance_entity
        try:
            await self.insurance_repository.create(
                session=self.session, data=command.insurance_entity.to_dict()
            )
            entity_event.register_event(
                EntityUpdatedEvent(
                    user_id=command.user_id,
                    status=Status.SUCCESS,
                    operation=Operation.CREATED,
                    cargo_type=entity_event.cargo_type,
                    rate=entity_event.rate,
                    date=entity_event.date,
                    event_title="update",
                )
            )
            return await self._event_mediator.publish(events=entity_event.pull_events())
        except IntegrityError:
            entity_event.register_event(
                EntityUpdatedEvent(
                    user_id=command.user_id,
                    status=Status.FAIL,
                    operation=Operation.CREATED,
                    cargo_type=entity_event.cargo_type,
                    rate=entity_event.rate,
                    date=entity_event.date,
                    event_title="update",
                )
            )
            return await self._event_mediator.publish(events=entity_event.pull_events())


class CreateInsuranceCommandHandler(BaseCommandHandler[CreateInsuranceCommand, CR]):
    insurance_repository: InsuranceRepository
    session: AsyncSession

    async def handle(self, command: CreateInsuranceCommand) -> CR:
        entity_event = command.insurance_entity
        try:
            await self.insurance_repository.create(
                session=self.session, data=command.insurance_entity.to_dict()
            )
            entity_event.register_event(
                EntityCreatedEvent(
                    user_id=command.user_id,
                    status=Status.SUCCESS,
                    operation=Operation.CREATED,
                    cargo_type=entity_event.cargo_type,
                    rate=entity_event.rate,
                    date=entity_event.date,
                    event_title="creation",
                )
            )
            return await self._event_mediator.publish(events=entity_event.pull_events())
        except IntegrityError:
            entity_event.register_event(
                EntityCreatedEvent(
                    user_id=command.user_id,
                    status=Status.FAIL,
                    operation=Operation.CREATED,
                    cargo_type=entity_event.cargo_type,
                    rate=entity_event.rate,
                    date=entity_event.date,
                    event_title="creation",
                )
            )
            return await self._event_mediator.publish(events=entity_event.pull_events())


class DeleteInsuranceCommandHandler(BaseCommandHandler[CreateInsuranceCommand, CR]):
    insurance_repository: InsuranceRepository
    session: AsyncSession

    async def handle(self, command: DeleteInsuranceCommand) -> CR:
        entity_event = command.insurance_entity
        try:
            await self.insurance_repository.create(
                session=self.session, data=command.insurance_entity.to_dict()
            )
            entity_event.register_event(
                EntityDeletedEvent(
                    user_id=command.user_id,
                    status=Status.SUCCESS,
                    operation=Operation.CREATED,
                    cargo_type=entity_event.cargo_type,
                    rate=entity_event.rate,
                    date=entity_event.date,
                    event_title="delete",
                )
            )
            return await self._event_mediator.publish(events=entity_event.pull_events())
        except IntegrityError:
            entity_event.register_event(
                EntityDeletedEvent(
                    user_id=command.user_id,
                    status=Status.FAIL,
                    operation=Operation.CREATED,
                    cargo_type=entity_event.cargo_type,
                    rate=entity_event.rate,
                    date=entity_event.date,
                    event_title="delete",
                )
            )
            return await self._event_mediator.publish(events=entity_event.pull_events())
