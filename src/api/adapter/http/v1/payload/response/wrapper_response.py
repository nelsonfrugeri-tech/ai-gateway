from src.api.adapter.http.v1.payload.common.base_payload import BasePayload
from typing import Optional, List, Any


class WrapperResponse(BasePayload):
    metadata: Optional[int] = None
    data: List[Any]
