from abc import ABC, abstractmethod
from src.api.adapter.http.v1.payload.request.batch_request import BatchRequest
from src.api.adapter.http.v1.payload.response.batch_response import BatchResponse


class BatchPort(ABC):
    @abstractmethod
    def generate(self, batch_request: BatchRequest) -> BatchResponse:
        pass

    @abstractmethod
    def get(self, model_name: str, batch_id: str) -> BatchResponse:
        pass
