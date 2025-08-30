from enum import Enum

from pydantic import ConfigDict
from src.api.adapter.http.v1.payload.common.base_payload import BasePayload
from src.api.adapter.http.v1.payload.request.common_request import Provider


class BatchCompletionWindowNameRequest(Enum):
    HOUR_24 = "24h"


class BatchCompletionWindowRequest(BasePayload):
    name: BatchCompletionWindowNameRequest


class BatchFileRequest(BasePayload):
    id: str


class BatchEndpointNameRequest(str, Enum):
    CHAT: str = "/chat/completions"


class BatchEndpointRequest(BasePayload):
    name: BatchEndpointNameRequest


class BatchRequest(BasePayload):
    file: BatchFileRequest
    completion_window: BatchCompletionWindowRequest
    provider: Provider
    endpoint: BatchEndpointRequest
    model_config = ConfigDict(arbitrary_types_allowed=True)
