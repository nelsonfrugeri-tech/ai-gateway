from typing import List, Optional
from src.api.adapter.http.v1.payload.common.base_payload import BasePayload
from src.api.adapter.http.v1.payload.response.cost_response import Cost, Usage


class EmbeddingResponse(BasePayload):
    data: List[list]
    usage: Usage
    cost: Optional[Cost] = None
