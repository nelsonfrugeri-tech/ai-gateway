from fastapi import APIRouter, Depends, status
from src.api.adapter.http.v1.header.base_header import BaseHeader
from src.api.adapter.http.v1.payload.request.embedding_request import EmbeddingRequest
from src.api.adapter.http.v1.payload.response.embedding_response import (
    EmbeddingResponse,
)
from src.api.core.business.embedding_business import EmbeddingBusiness
from src.api.adapter.http.v1.payload.response.error_response import ErrorResponse

embedding_router = APIRouter()
embedding_business = EmbeddingBusiness()


@embedding_router.post(
    "/v1/embeddings",
    response_model=EmbeddingResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request",
            "model": ErrorResponse,
        }
    },
)
def embedding(
    embedding_request: EmbeddingRequest,
    headers: BaseHeader = Depends(BaseHeader.validate),
) -> EmbeddingRequest:
    return embedding_business.generate_embedding(embedding_request)
