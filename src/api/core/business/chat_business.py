from src.api.adapter.http.v1.payload.request.chat_request import ChatRequest
from src.api.adapter.service.provider.port.chat_port import ChatPort
from src.api.adapter.service.provider.service_provider import ServiceProvider
from src.api.adapter.http.v1.payload.request.image_request import ImageRequest


class ChatBusiness:

    def __init__(self):
        self.service_provider = ServiceProvider()

    def generate_text(self, chat_request: ChatRequest) -> ChatPort:
        return self.service_provider.generate_text(
            provider_name=chat_request.provider.name,
            chat_request=chat_request,
        )

    def generate_text_stream(self, chat_request_stream: ChatRequest) -> ChatPort:
        return self.service_provider.generate_text_stream(
            provider_name=chat_request_stream.provider.name,
            chat_request=chat_request_stream,
        )

    def generate_image(self, image_request: ImageRequest) -> ChatPort:
        return self.service_provider.generate_image(
            provider_name=image_request.provider.name,
            image_request=image_request,
        )
