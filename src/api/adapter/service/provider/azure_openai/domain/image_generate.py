from pydantic import BaseModel
from typing import Optional


class ImageGenerate(BaseModel):
    prompt: str
    model: str
    n: Optional[int]
    quality: Optional[str]
    response_format: Optional[str]
    size: Optional[str]
    style: Optional[str]
