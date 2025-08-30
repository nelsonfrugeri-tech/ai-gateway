from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from src.api.adapter.http.v1.payload.response.guardrail_response import (
    GuardrailResponse,
)


class Image(BaseModel):
    b64_json: Optional[str] = None
    revised_prompt: Optional[str] = None
    url: Optional[HttpUrl] = None
    guardrail: Optional[GuardrailResponse] = None


class ImageResponse(BaseModel):
    data: List[Image]
