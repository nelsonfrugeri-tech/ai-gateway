from collections import namedtuple
from enum import Enum
from uuid import UUID, uuid4
from pydantic import Field, ConfigDict, field_serializer
from typing import List, Optional
from src.api.adapter.http.v1.payload.common.base_payload import BasePayload


def serialize_enum(value: Enum):
    return {"id": value.id, "name": value.name, "description": value.description}


class EndpointName(str, Enum):
    CHAT: str = "/chat/completions"


class Endpoint(BasePayload):
    name: EndpointName = EndpointName.CHAT

    model_config = ConfigDict(use_enum_values=True)


class ProcessType(str, Enum):
    REALTIME = "real_time"
    BATCH = "batch"
    STREAM = "stream"


class ImageQuality(Enum):
    STANDARD = "Standard"
    HD = "HD"


class UnitOfMeasure(Enum):
    MILLION = 1000000
    THOUSAND = 1000


class Currency(Enum):
    USD = "USD"
    BRL = "R$"


class Pixel(BasePayload):
    width: int
    height: int
    quality: Optional[ImageQuality] = None
    value: float


class Token(BasePayload):
    input_value: float
    output_value: Optional[float] = None
    training_value: Optional[float] = None


class Price(BasePayload):
    id: UUID = Field(default_factory=uuid4)
    unit_of_measure: Optional[UnitOfMeasure] = UnitOfMeasure.MILLION
    currency: Optional[Currency] = Currency.USD
    pixel: Optional[Pixel] = None
    token: Optional[Token] = None


EnumFields = namedtuple("EnumFields", ["id", "name", "description"])


class CategoryResponse(BasePayload):
    generation_type: Enum
    modal_type: Enum

    @field_serializer("generation_type")
    def serialize_generation_type(self, value: Enum):
        return serialize_enum(value.value)

    @field_serializer("modal_type")
    def serialize_modal_type(self, value: Enum):
        return serialize_enum(value.value)


class Model(BasePayload):
    id: UUID = Field(default_factory=uuid4)
    name: str
    label: str
    description: str
    context_window: Optional[int]
    training_data: Optional[str]
    prices: Optional[List[Price]] = None
    endpoints: Optional[List[Endpoint]] = None
    enabled: bool
    category: CategoryResponse
    process_type: Optional[List[ProcessType]] = None


class ProviderResponse(BasePayload):
    id: UUID = Field(default_factory=uuid4)
    name: str
    label: str
    description: str
    models: List[Model]
