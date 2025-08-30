import os
from fastapi import Header
from pydantic import UUID4, Field
from uuid import UUID
from src.api.adapter.http.v1.header.base_header import BaseHeader
from src.api.core.exception.unauthorized_exception import (
    UnauthorizedException,
)


class QuotaHeader(BaseHeader):
    x_admin_auth: UUID4 = Field(None, alias="X-Admin-Auth")

    @classmethod
    def validate(
        cls,
        x_correlation_id: UUID4 = Header(None, alias="X-Correlation-Id"),
        x_user_id: str = Header(None, alias="X-User-Id"),
        client_id: UUID4 = Header(None, alias="client_id"),
        x_admin_auth: UUID4 = Header(None, alias="X-Admin-Auth"),
    ) -> "QuotaHeader":
        super().validate(x_correlation_id, x_user_id, client_id)

        genai_quota_auth = os.getenv("GENAI_QUOTA_AUTHENTICATION", None)

        if genai_quota_auth is not None and isinstance(genai_quota_auth, str):
            genai_quota_auth = UUID(genai_quota_auth)

        if x_admin_auth != genai_quota_auth or not x_admin_auth:
            raise UnauthorizedException("The X-Admin-Auth is invalid.")

        return cls(
            x_correlation_id=x_correlation_id,
            x_user_id=x_user_id,
            client_id=client_id,
            x_admin_auth=x_admin_auth,
        )
