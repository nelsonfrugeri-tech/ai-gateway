from datetime import datetime
from enum import Enum

from pydantic import Field, ConfigDict

from src.api.adapter.http.v1.payload.common.base_payload import BasePayload


class QuotaUnitResponse(Enum):
    TOKENS = "tokens"


class ModelResponse(BasePayload):
    name: str


class ProviderResponse(BasePayload):
    name: str
    model: ModelResponse


class UseCaseResponse(BasePayload):
    id: str
    name: str


class QuotaResponse(BasePayload):
    id: str
    unit: QuotaUnitResponse
    limit: int
    balance: int
    use_case: UseCaseResponse
    provider: ProviderResponse
    created_at: datetime
    enabled: bool

    @classmethod
    def from_dict(cls, data: dict) -> "QuotaResponse":
        return cls(**data)

