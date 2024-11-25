from datetime import date

from pydantic import RootModel, BaseModel, Field

from src.common.converters.converter import convert_to_int
from src.domain.entitites.tariff_entities import TariffEntityWithConvertRate


class CargoItem(BaseModel):
    cargo_type: str
    rate: float = Field(ge=0.00001, description="Rate must be greater than 0")


class CargoRateSchema(RootModel[dict[date, list[CargoItem]]]):
    def to_entities(self) -> list[TariffEntityWithConvertRate]:
        entities = []
        for date_key, rate_items in self.root.items():
            for item in rate_items:
                try:
                    rate, divide_rate_convert = convert_to_int(item.rate)
                    entities.append(TariffEntityWithConvertRate(
                        date=date_key,
                        cargo_type=item.cargo_type,
                        rate=rate,
                        divide_rate_convert=divide_rate_convert,
                    ))
                except (TypeError, ValueError):
                    continue
        return entities


class TariffItem(CargoItem):
    date: date

    def to_entities(self) -> TariffEntityWithConvertRate:
        rate, divide_rate_convert = convert_to_int(self.rate)
        return TariffEntityWithConvertRate(
            date=self.date,
            cargo_type=self.cargo_type,
            rate=rate,
            divide_rate_convert=divide_rate_convert,
        )

