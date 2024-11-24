from dataclasses import dataclass

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entitites.base import Status, Operation
from src.domain.entitites.insurance_entities import (
    InsuranceEntityIn,
)
from src.infra.repository.insurance_repository import InsuranceRepository
from src.logic.comands.base import BaseCommand, BaseCommandHandler, CR
from src.logic.events.events import EntityCreatedEvent


@dataclass(eq=False)
class CreateInsuranceCommand(BaseCommand):
    insurance_entity: InsuranceEntityIn


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
                    status=Status.FAIL,
                    operation=Operation.CREATED,
                    cargo_type=entity_event.cargo_type,
                    rate=entity_event.rate,
                    date=entity_event.date,
                    event_title="Creation",
                )
            )
            return await self._event_mediator.publish(events=entity_event.pull_events())
