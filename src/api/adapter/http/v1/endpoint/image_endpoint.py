from fastapi import APIRouter, Depends, status
from src.api.adapter.http.v1.header.base_header import BaseHeader
from src.api.adapter.http.v1.payload.request.image_request import ImageRequest
from src.api.adapter.http.v1.payload.response.image_response import ImageResponse
from src.api.core.business.chat_business import ChatBusiness
from src.api.adapter.http.v1.payload.response.error_response import ErrorResponse


image_router = APIRouter()
chat_business = ChatBusiness()


@image_router.post(
    "/v1/images/generations",
    response_model=ImageResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request",
            "model": ErrorResponse,
        }
    },
)
def images_generations(
    image_request: ImageRequest = Depends(ImageRequest.validate),
    headers: BaseHeader = Depends(BaseHeader.validate),
) -> ImageRequest:
    return chat_business.generate_image(image_request)
