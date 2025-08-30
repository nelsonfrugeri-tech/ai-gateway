from enum import Enum
from typing import Optional
from pydantic import field_validator
from src.api.adapter.http.v1.payload.common.base_payload import BasePayload


class Currency(Enum):
    USD = "USD"
    BRL = "R$"


class UnitOfMeasure(Enum):
    MILLION = 1000000
    THOUSAND = 1000


class Pixel(BasePayload):
    total: float


class Price(BasePayload):
    unit_of_measure: Optional[UnitOfMeasure] = UnitOfMeasure.MILLION
    currency: Optional[Currency] = Currency.USD
    input_value: float
    output_value: Optional[float] = None


class Token(BasePayload):
    price: Price
    completion: Optional[float] = None
    prompt: Optional[float] = None
    total: float

    @field_validator("completion", "prompt")
    def round_to_six_decimal_places(cls, value):
        return round(value, 6)


class Cost(BasePayload):
    pixel: Optional[Pixel] = None
    token: Optional[Token] = None


class Usage(BasePayload):
    completion_tokens: Optional[int] = None
    prompt_tokens: int
    total_tokens: int
