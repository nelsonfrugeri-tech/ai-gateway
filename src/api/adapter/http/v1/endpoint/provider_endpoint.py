from fastapi import APIRouter, Depends, status
from src.api.adapter.http.v1.header.base_header import BaseHeader
from src.api.adapter.http.v1.payload.response.wrapper_response import WrapperResponse
from src.api.adapter.http.v1.mapper.provider_mapper import ProviderMapper
from src.api.adapter.http.v1.payload.response.error_response import ErrorResponse
from src.api.adapter.cache.simple.provider_cache import ProviderCache


provider_router = APIRouter(prefix="/v1")
provider_mapper = ProviderMapper()


@provider_router.get(
    "/providers",
    response_model=WrapperResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request",
            "model": ErrorResponse,
        }
    },
)
def provider(headers: BaseHeader = Depends(BaseHeader.validate)):
    providers = ProviderCache.get_providers()
    providers_response = provider_mapper.to_providers(providers)
    return WrapperResponse(data=providers_response)
