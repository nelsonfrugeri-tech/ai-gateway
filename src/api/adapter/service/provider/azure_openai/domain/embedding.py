from pydantic import BaseModel
from typing import List


class Embedding(BaseModel):
    input: List[str]
    model: str
