from typing import Optional
from fastapi import APIRouter, Depends, Query
from src.api.adapter.http.v1.payload.response.wrapper_response import WrapperResponse
from src.api.adapter.http.v1.payload.response.error_response import ErrorResponse
from src.api.adapter.validation.provider_validation import ProviderValidation
from src.api.adapter.validation.model_validation import ModelValidation


from src.api.adapter.http.v1.header.base_header import BaseHeader
from src.api.adapter.http.v1.header.quota_header import QuotaHeader
from src.api.adapter.http.v1.payload.request.quota_request import (
    QuotaRequest,
    QuotaUpdateRequest,
)
from src.api.adapter.http.v1.payload.response.quota_response import (
    QuotaResponse,
)
from src.api.core.business.quota_business import QuotaBusiness
from fastapi import Request

quota_router = APIRouter()


@quota_router.post(
    "/v1/quotas",
    response_model=QuotaResponse,
    response_model_exclude_none=True,
    status_code=201,
    responses={400: {"description": "Bad Request", "model": ErrorResponse}},
)
async def create(
    request: Request,
    quota_request: QuotaRequest,
    headers: QuotaHeader = Depends(QuotaHeader.validate),
) -> QuotaResponse:
    return await QuotaBusiness(request.app.state.db).create(quota_request)


@quota_router.get(
    "/v1/quotas",
    response_model=WrapperResponse,
    response_model_exclude_none=True,
    status_code=200,
    responses={400: {"description": "Bad Request", "model": ErrorResponse}},
)
async def retrieve(
    request: Request,
    use_case_id: str = Query(..., alias="useCaseId", min_length=1, regex=r"^\S+$"),
    enabled: Optional[bool] = None,
    provider_name: str = Depends(ProviderValidation.validate_provider_existence),
    model_name: str = Depends(ModelValidation.validate_model_existence),
    headers: BaseHeader = Depends(BaseHeader.validate),
) -> QuotaRequest:
    return WrapperResponse(
        data=await QuotaBusiness(request.app.state.db).retrieve(
            use_case_id=use_case_id,
            provider_name=provider_name,
            model_name=model_name,
            enabled=enabled,
        )
    )


@quota_router.patch(
    "/v1/quotas",
    response_model=QuotaResponse,
    response_model_exclude_none=True,
    status_code=200,
    responses={400: {"description": "Bad Request", "model": ErrorResponse}},
)
async def update(
    request: Request,
    quota_request: QuotaUpdateRequest,
    use_case_id: str = Query(..., alias="useCaseId", min_length=1, regex=r"^\S+$"),
    enabled: Optional[bool] = None,
    provider_name: str = Depends(ProviderValidation.validate_provider_existence),
    model_name: str = Depends(ModelValidation.validate_model_existence),
    headers: QuotaHeader = Depends(QuotaHeader.validate),
) -> QuotaResponse:
    return await QuotaBusiness(request.app.state.db).update(
        use_case_id=use_case_id,
        provider_name=provider_name,
        model_name=model_name,
        quota_request=quota_request,
        enabled=enabled,
    )
