from enum import Enum
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from typing import Optional


class ImageQuality(Enum):
    STANDARD = "Standard"
    HD = "HD"


class UnitOfMeasure(Enum):
    MILLION = 1000000
    THOUSAND = 1000


class Currency(Enum):
    USD = "USD"
    BRL = "R$"


class Pixel(BaseModel):
    width: int
    height: int
    quality: Optional[ImageQuality] = None
    value: float


class Token(BaseModel):
    input_value: float
    output_value: Optional[float] = None
    tranning_value: Optional[float] = None


class Price(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    unit_of_measure: Optional[UnitOfMeasure] = UnitOfMeasure.MILLION
    currency: Optional[Currency] = Currency.USD
    pixel: Optional[Pixel] = None
    token: Optional[Token] = None
