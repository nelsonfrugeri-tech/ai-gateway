from pydantic import BaseModel, field_serializer
from typing import Optional
from datetime import datetime


class ExceptionDetail(BaseModel):
    type: str
    message: str
    stack_trace: Optional[str] = None


class Application(BaseModel):
    name: str
    version: str


class Environment(BaseModel):
    hostname: str
    ip: str
    runtime: str
    platform: str


class Request(BaseModel):
    method: str
    url: str
    headers: dict
    body: Optional[dict] = None


class Response(BaseModel):
    status_code: int
    body: Optional[dict] = None
    latency: float


class HTTPLog(BaseModel):
    level: str
    correlation_id: str
    timestamp: datetime
    message: str
    application: Application
    environment: Environment
    request: Request
    response: Optional[Response] = None
    exception: Optional[ExceptionDetail] = None

    @field_serializer("timestamp")
    def serialize_dt(self, value: datetime, _info):
        return value.isoformat()
