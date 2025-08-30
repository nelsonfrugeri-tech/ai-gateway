from fastapi import APIRouter, Depends, Path, status
from src.api.adapter.http.v1.header.base_header import BaseHeader
from src.api.adapter.validation.provider_validation import ProviderValidation
from src.api.adapter.validation.model_validation import ModelValidation
from src.api.adapter.http.v1.payload.request.batch_request import BatchRequest
from src.api.adapter.http.v1.payload.response.batch_response import (
    BatchResponse,
)
from src.api.core.business.batch_business import BatchBusiness
from src.api.adapter.http.v1.payload.response.error_response import ErrorResponse

batch_router = APIRouter()
batch_business = BatchBusiness()


@batch_router.post(
    "/v1/batches",
    response_model=BatchResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request",
            "model": ErrorResponse,
        }
    },
)
def batch(
    batch_request: BatchRequest,
    headers: BaseHeader = Depends(BaseHeader.validate),
) -> BatchRequest:
    return batch_business.generate_batch(batch_request)


@batch_router.get(
    "/v1/batches/{batchId}",
    response_model=BatchResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request",
            "model": ErrorResponse,
        }
    },
)
def get_batch(
    batch_id: str = Path(..., alias="batchId"),
    provider_name: str = Depends(ProviderValidation.validate_provider_existence),
    model_name: str = Depends(ModelValidation.validate_model_existence),
    headers: BaseHeader = Depends(BaseHeader.validate),
) -> BatchRequest:
    return batch_business.get_batch(provider_name, model_name, batch_id)
