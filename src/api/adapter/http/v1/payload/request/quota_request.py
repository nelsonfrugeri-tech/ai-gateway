from enum import Enum

from pydantic import PositiveInt, Field
from pydantic.v1 import ConfigDict
from src.api.adapter.http.v1.payload.common.base_payload import BasePayload


class QuotaUnitRequest(Enum):
    TOKENS = "tokens"


class ModelRequest(BasePayload):
    name: str = Field(min_length=1)
    model_config = ConfigDict(str_strip_whitespace=True)


class ProviderRequest(BasePayload):
    name: str = Field(min_length=1)
    model: ModelRequest

    model_config = ConfigDict(str_strip_whitespace=True)


class UseCaseRequest(BasePayload):
    id: str = Field(min_length=1)
    name: str

    model_config = ConfigDict(str_strip_whitespace=True)


class QuotaUpdateRequest(BasePayload):
    enabled: bool


class QuotaRequest(BasePayload):
    unit: QuotaUnitRequest
    limit: PositiveInt
    use_case: UseCaseRequest
    provider: ProviderRequest


