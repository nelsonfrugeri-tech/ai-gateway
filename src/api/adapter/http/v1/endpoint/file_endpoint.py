from fastapi import APIRouter, Depends, Path, status
from src.api.adapter.validation.provider_validation import ProviderValidation
from src.api.adapter.validation.model_validation import ModelValidation
from src.api.adapter.http.v1.header.base_header import BaseHeader
from src.api.adapter.http.v1.payload.request.file_request import (
    FileRequest,
)
from src.api.adapter.http.v1.payload.response.file_response import FileResponse
from src.api.core.business.file_business import FileBusiness
from src.api.adapter.http.v1.payload.response.error_response import ErrorResponse

file_router = APIRouter()
file_business = FileBusiness()


@file_router.post(
    "/v1/files",
    response_model=FileResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request",
            "model": ErrorResponse,
        }
    },
)
def create_file(
    file_request: FileRequest,
    headers: BaseHeader = Depends(BaseHeader.validate),
) -> FileRequest:
    return file_business.generate_file(file_request)


@file_router.get(
    "/v1/files/{fileId}",
    response_model=FileResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request",
            "model": ErrorResponse,
        }
    },
)
def get_file(
    file_id: str = Path(..., alias="fileId"),
    provider_name: str = Depends(ProviderValidation.validate_provider_existence),
    model_name: str = Depends(ModelValidation.validate_model_existence),
    headers: BaseHeader = Depends(BaseHeader.validate),
) -> FileRequest:
    return file_business.get_file(provider_name, model_name, file_id)
