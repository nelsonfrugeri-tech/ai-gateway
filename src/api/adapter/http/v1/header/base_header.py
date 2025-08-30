from fastapi import Header
from pydantic import BaseModel, UUID4, Field
from typing import Optional

from src.api.core.exception.bad_request_exception import BadRequestException


class BaseHeader(BaseModel):
    x_correlation_id: Optional[UUID4] = Field(None, alias="X-Correlation-Id")
    x_user_id: Optional[str] = Field(None, alias="X-User-Id")
    client_id: Optional[UUID4] = Field(None, alias="client_id")

    @classmethod
    def validate(
        cls,
        x_correlation_id: UUID4 = Header(None, alias="X-Correlation-Id"),
        x_user_id: str = Header(None, alias="X-User-Id"),
        client_id: UUID4 = Header(None, alias="client_id"),
    ) -> "BaseHeader":
        missing_params = []

        if x_correlation_id is None:
            missing_params.append("The X-Correlation-Id header field is required")
        if x_user_id is None:
            missing_params.append("The X-User-Id header field is required")
        if client_id is None:
            missing_params.append("The client_id header field is required")

        if len(missing_params) > 0:
            raise BadRequestException(params=missing_params)
        return cls(
            x_correlation_id=x_correlation_id, x_user_id=x_user_id, client_id=client_id
        )
