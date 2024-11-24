from dataclasses import dataclass

from src.domain.entitites.insurance_entities import InsuranceEntityIn
from src.logic.comands.base import BaseCommand, BaseCommandHandler


@dataclass(eq=False)
class CreateInsuranceCommand(BaseCommand):
    insurance_entity: InsuranceEntityIn


@dataclass(eq=False)
class CreateInsuranceCommand(BaseCommand):
    insurance_entity: InsuranceEntityIn


class CreateInsuranceCommandHandler(BaseCommandHandler):...
