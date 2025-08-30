from abc import ABC, abstractmethod
from src.api.adapter.http.v1.payload.request.image_request import ImageRequest
from src.api.adapter.http.v1.payload.response.image_response import ImageResponse


class ImagePort(ABC):
    @abstractmethod
    def generate(self, image_request: ImageRequest) -> ImageResponse:
        pass
