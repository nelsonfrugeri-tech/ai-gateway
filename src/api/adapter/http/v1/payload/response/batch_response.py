from collections import namedtuple
from datetime import datetime
from enum import Enum
from pydantic import field_validator, field_serializer, ConfigDict
from typing import Optional, List
from src.api.adapter.http.v1.payload.common.base_payload import BasePayload
from src.api.adapter.http.v1.payload.response.cost_response import Cost

EnumFields = namedtuple("EnumFields", ["id", "name", "description"])


def serialize_enum(value: Enum):
    return {"id": value.id, "name": value.name, "description": value.description}


class BatchMessageResponse(BasePayload):
    role: str
    content: str


class BatchUsageResponse(BasePayload):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int


class BatchStatusResponse(Enum):
    validating = EnumFields(1, "validating", "Batch process is being validated")
    failed = EnumFields(2, "failed", "Batch process has failed")
    in_progress = EnumFields(3, "in_progress", "Batch in progress")
    finalizing = EnumFields(4, "finalizing", "Batch is being finalized")
    completed = EnumFields(5, "completed", "Batch process completed successfully")
    expired = EnumFields(6, "expired", "Batch has expired")
    cancelling = EnumFields(7, "cancelling", "Batch process is being cancelled")
    cancelled = EnumFields(8, "cancelled", "Batch process has been cancelled")


class BatchEndpointResponse(Enum):
    chat = EnumFields(1, "/chat/completions", "Chat Conversation")

    @classmethod
    def from_endpoint(cls, name: str):
        for member in cls:
            if member.value.name == name:
                return member
        return None


class BatchCompletionWindowNameResponse(Enum):
    HOUR_24 = "24h"


class BatchRequestCountsResponse(BasePayload):
    total: int
    completed: int
    failed: int


class BatchFileResponse(BasePayload):
    id: str


class BatchCompletionWindowResponse(BasePayload):
    name: BatchCompletionWindowNameResponse


class BatchResultTypeResponse(Enum):
    BASE_64 = "base64"


class BatchResultResponse(BasePayload):
    type: BatchResultTypeResponse
    content: str


class BatchErrorResponse(BasePayload):
    code: str
    message: str
    line: Optional[int] = None


class BatchDataItemResponse(BasePayload):
    message: BatchMessageResponse
    usage: BatchUsageResponse
    error: Optional[BatchErrorResponse] = None


class BatchDataResponse(BasePayload):
    data: List[BatchDataItemResponse]

    model_config = ConfigDict(arbitrary_types_allowed=True)


class BatchResponse(BasePayload):
    id: str
    file: BatchFileResponse
    status: BatchStatusResponse
    request_counts: BatchRequestCountsResponse
    completion_window: BatchCompletionWindowResponse
    endpoint: BatchEndpointResponse
    errors: Optional[List[BatchErrorResponse]] = None
    cost: Optional[Cost] = None
    usage: Optional[BatchUsageResponse] = None
    result: Optional[BatchResultResponse] = None
    created_at: Optional[datetime] = None
    in_progress_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    failed_at: Optional[datetime] = None
    expired_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator(
        "created_at",
        "in_progress_at",
        "completed_at",
        "failed_at",
        "expired_at",
        "cancelled_at",
        mode="before",
    )
    def convert_epoch_to_datetime(cls, value):
        if value is None:
            return None
        return datetime.fromtimestamp(value)

    @field_serializer("status", "endpoint")
    def serialize_extension(self, value):
        return serialize_enum(value.value)
