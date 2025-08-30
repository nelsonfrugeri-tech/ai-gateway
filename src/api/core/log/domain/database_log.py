from enum import Enum
from pydantic import BaseModel, field_serializer, ConfigDict

from datetime import datetime
from typing import Optional, List, Any


class OperatorUpdateLogging(Enum):
    SET = "$set"


class OperationNameLogging(Enum):
    INSERT_ONE = "insert_one"
    FIND_ONE_AND_UPDATE = "find_one_and_update"
    UPDATE_MANY = "update_many"
    FIND = "find"


class OperatorUpdateValueLogging(BaseModel):
    key: str
    value: Any


class LatencyLogging(BaseModel):
    time: float
    unit: str = "ms"

    @field_serializer("time")
    def round_time(self, value: float):
        return round(value, 2)


class ExceptionLogging(BaseModel):
    type: str
    message: str
    stack_trace: Optional[str] = None


class UseCaseLogging(BaseModel):
    id: str
    name: Optional[str] = None


class ModelLogging(BaseModel):
    name: str


class ProviderLogging(BaseModel):
    name: str
    model: ModelLogging


class QueryLogging(BaseModel):
    provider: ProviderLogging
    use_case: UseCaseLogging
    enabled: Optional[bool] = None


class DocumentLogging(BaseModel):
    unit: str
    limit: int
    balance: int
    use_case: UseCaseLogging
    provider: ProviderLogging
    created_at: datetime
    enabled: bool

    model_config = ConfigDict(
        use_enum_values=True,
    )

    @field_serializer("created_at")
    def serialize_dt(self, value: datetime, _info):
        return value.isoformat()


class DocumentResponseLogging(BaseModel):
    id: str


class UpdateLogging(BaseModel):
    operator: OperatorUpdateLogging
    update_values: List[OperatorUpdateValueLogging]

    model_config = ConfigDict(
        use_enum_values=True,
    )


class UpdateResponseLogging(BaseModel):
    matched_count: int


class ResponseLogging(BaseModel):
    documents: Optional[List[DocumentResponseLogging]] = None
    update: Optional[UpdateResponseLogging] = None
    latency: LatencyLogging


class OperationLogging(BaseModel):
    name: OperationNameLogging
    documents: Optional[List[DocumentLogging]] = None
    query: Optional[QueryLogging] = None
    updates: Optional[List[UpdateLogging]] = None
    response: ResponseLogging

    model_config = ConfigDict(use_enum_values=True)


class VendorLogging(BaseModel):
    name: str
    version: str


class DatabaseLog(BaseModel):
    level: str
    correlation_id: str
    timestamp: datetime
    vendor: VendorLogging
    operation: OperationLogging
    exception: Optional[ExceptionLogging] = None

    @field_serializer("timestamp")
    def serialize_dt(self, value: datetime, _info):
        return value.isoformat()
