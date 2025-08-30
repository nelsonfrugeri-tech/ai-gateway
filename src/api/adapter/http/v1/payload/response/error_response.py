from pydantic import BaseModel
from typing import Optional, List


class ErrorDetails(BaseModel):
    statusCode: str
    message: str
    details: Optional[List[str]] = None


class ErrorResponse(BaseModel):
    errorDetails: List[ErrorDetails]
