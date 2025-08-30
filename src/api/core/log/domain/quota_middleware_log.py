from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_serializer


class ExceptionLogging(BaseModel):
    type: str
    message: str
    stack_trace: Optional[str] = None


class ModelLogging(BaseModel):
    name: str


class ProviderLogging(BaseModel):
    name: str
    model: ModelLogging


class UsageLogging(BaseModel):
    completion_tokens: Optional[int] = None
    prompt_tokens: int
    total_tokens: int


class LatencyLogging(BaseModel):
    time: float
    unit: str = "ms"

    @field_serializer("time")
    def round_time(self, value: float):
        return round(value, 2)


class RequestLogging(BaseModel):
    path: str
    method: str


class ResponseLogging(BaseModel):
    status_code: int
    latency: LatencyLogging


class QuotaLogging(BaseModel):
    usage: UsageLogging
    provider: ProviderLogging
    limit: int
    balance: int
    new_balance: int


class QuotaMiddlewareLog(BaseModel):
    level: str
    correlation_id: str
    timestamp: datetime
    request: Optional[RequestLogging] = None
    response: Optional[ResponseLogging] = None
    quota: Optional[QuotaLogging] = None
    exception: Optional[ExceptionLogging] = None

    @field_serializer("timestamp")
    def serialize_dt(self, value: datetime, _info):
        return value.isoformat()
