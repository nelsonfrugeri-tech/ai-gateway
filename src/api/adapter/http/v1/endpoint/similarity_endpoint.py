from fastapi import APIRouter, Depends, status
from src.api.adapter.http.v1.header.base_header import BaseHeader
from src.api.adapter.http.v1.payload.request.similarity_request import SimilarityRequest
from src.api.adapter.http.v1.payload.response.similarity_response import (
    SimilarityResponse,
)
from src.api.core.business.similarity_business import SimilarityBusiness
from src.api.adapter.http.v1.payload.response.error_response import ErrorResponse

similarity_router = APIRouter()
similarity_business = SimilarityBusiness()


@similarity_router.post(
    "/v1/similarity",
    response_model=SimilarityResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request",
            "model": ErrorResponse,
        }
    },
)
def generate_similarity(
    similarity_request: SimilarityRequest,
    headers: BaseHeader = Depends(BaseHeader.validate),
) -> SimilarityRequest:
    return similarity_business.generate_similarity(similarity_request)
