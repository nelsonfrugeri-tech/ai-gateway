from pydantic import field_validator
from typing import List, Optional
from src.api.adapter.http.v1.payload.common.base_payload import BasePayload
from src.api.adapter.http.v1.payload.response.cost_response import Cost, Usage


class ResultResponse(BasePayload):
    embedding: List[float]
    text: str


class SimilarityResponse(BasePayload):
    results: List[ResultResponse]
    score: float
    usage: Usage
    cost: Optional[Cost] = None

    @field_validator("score", mode="before")
    def round_score(cls, value):
        if value is not None:
            return round(value, 6)
        return value
