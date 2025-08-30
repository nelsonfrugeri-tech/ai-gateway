from abc import ABC, abstractmethod
from src.api.adapter.http.v1.payload.request.chat_request import ChatRequest
from src.api.adapter.http.v1.payload.response.chat_response import ChatResponse


class ChatPort(ABC):
    @abstractmethod
    def generate(self, chat_request: ChatRequest) -> ChatResponse:
        pass

    @abstractmethod
    async def generate_stream(self, chat_request: ChatRequest):
        pass
