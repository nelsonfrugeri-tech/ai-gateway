from enum import Enum
from pydantic import ConfigDict
from src.api.adapter.http.v1.payload.common.base_payload import BasePayload


class BatchCompletionWindow(Enum):
    HOUR_24 = "24h"


class Batch(BasePayload):
    input_file_id: str
    endpoint: str
    completion_window: BatchCompletionWindow
    model: str

    model_config = ConfigDict(arbitrary_types_allowed=True, use_enum_values=True)
