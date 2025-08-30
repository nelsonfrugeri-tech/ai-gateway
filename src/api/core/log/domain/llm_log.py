from pydantic import BaseModel, field_serializer
from typing import Optional
from datetime import datetime


class LatencyLogging(BaseModel):
    time: float
    unit: str = "ms"


class ExceptionDetailLogging(BaseModel):
    type: str
    message: str
    stack_trace: Optional[str] = None


class ResponseLogging(BaseModel):
    status_code: int
    latency: LatencyLogging
    exception: Optional[ExceptionDetailLogging] = None


class CallLogging(BaseModel):
    response: ResponseLogging


class AzureOpenAIClientLogging(BaseModel):
    base_url: str
    api_version: str


class ProviderLogging(BaseModel):
    name: str
    model: str
    client: AzureOpenAIClientLogging
    call: CallLogging


class LLMLog(BaseModel):
    level: str
    correlation_id: str
    timestamp: datetime
    provider: ProviderLogging

    @field_serializer("timestamp")
    def serialize_dt(self, value: datetime, _info):
        return value.isoformat()
