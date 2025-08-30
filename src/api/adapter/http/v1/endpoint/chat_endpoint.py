from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse
from src.api.adapter.http.v1.header.base_header import BaseHeader
from src.api.adapter.http.v1.payload.request.chat_request import ChatRequest
from src.api.adapter.http.v1.payload.response.chat_response import ChatResponse
from src.api.core.business.chat_business import ChatBusiness
from src.api.adapter.http.v1.payload.response.error_response import ErrorResponse

chat_router = APIRouter()
chat_business = ChatBusiness()


@chat_router.post(
    "/v1/chat",
    response_model=ChatResponse,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request",
            "model": ErrorResponse,
        }
    },
)
def chat(
    chat_request: ChatRequest = Depends(ChatRequest.validate),
    headers: BaseHeader = Depends(BaseHeader.validate),
) -> ChatRequest:
    return chat_business.generate_text(chat_request)


@chat_router.post(
    "/v1/chat/stream",
    response_model=ChatRequest,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request",
            "model": ErrorResponse,
        }
    },
)
async def chat_stream(
    chat_request: ChatRequest = Depends(ChatRequest.validate),
    headers: BaseHeader = Depends(BaseHeader.validate),
) -> StreamingResponse:
    return StreamingResponse(
        chat_business.generate_text_stream(chat_request), media_type="text/event-stream"
    )
