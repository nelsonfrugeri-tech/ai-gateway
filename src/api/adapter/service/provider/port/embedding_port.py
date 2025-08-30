from abc import ABC, abstractmethod
from src.api.adapter.http.v1.payload.request.embedding_request import EmbeddingRequest
from src.api.adapter.http.v1.payload.response.embedding_response import (
    EmbeddingResponse,
)


class EmbeddingPort(ABC):
    @abstractmethod
    def generate(self, embedding_request: EmbeddingRequest) -> EmbeddingResponse:
        pass
