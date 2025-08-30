from abc import ABC, abstractmethod
from typing import Union
from src.api.adapter.http.v1.payload.response.chat_response import ChatResponse
from src.api.adapter.http.v1.payload.response.embedding_response import (
    EmbeddingResponse,
)
from src.api.adapter.http.v1.payload.response.image_response import ImageResponse
from src.api.domain.price import Price


class InterfaceCost(ABC):
    @abstractmethod
    def calculate_cost(
        self,
        price: Price,
        response: Union[ChatResponse, EmbeddingResponse, ImageResponse],
    ) -> Union[ChatResponse, EmbeddingResponse, ImageResponse]:
        pass
