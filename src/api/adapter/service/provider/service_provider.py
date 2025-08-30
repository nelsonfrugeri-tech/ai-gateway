from src.api.adapter.http.v1.payload.request.chat_request import ChatRequest
from src.api.adapter.service.provider.azure_openai.drive.azure_openai_drive import (
    AzureOpenAIDrive,
)
from src.api.adapter.service.provider.port.chat_port import ChatPort
from src.api.adapter.service.provider.port.image_port import ImagePort
from src.api.adapter.service.provider.port.embedding_port import EmbeddingPort
from src.api.adapter.service.provider.port.file_port import FilePort
from src.api.adapter.service.provider.port.batch_port import BatchPort
from src.api.adapter.http.v1.payload.request.image_request import ImageRequest
from src.api.adapter.http.v1.payload.request.embedding_request import EmbeddingRequest
from src.api.adapter.http.v1.payload.request.batch_request import BatchRequest
from src.api.domain.file import File


class ServiceProvider:
    def __init__(self):
        self.providers = {
            "azure_openai": AzureOpenAIDrive(),
        }

    def generate_text(self, provider_name: str, chat_request: ChatRequest) -> ChatPort:
        return self.providers[provider_name].generate_text(chat_request)

    def generate_text_stream(
        self, provider_name: str, chat_request: ChatRequest
    ) -> ChatPort:
        return self.providers[provider_name].generate_text_stream(chat_request)

    def generate_image(
        self, provider_name: str, image_request: ImageRequest
    ) -> ImagePort:
        return self.providers[provider_name].generate_image(image_request)

    def generate_embedding(
        self, provider_name: str, embedding_request: EmbeddingRequest
    ) -> EmbeddingPort:
        return self.providers[provider_name].generate_embedding(embedding_request)

    def generate_file(self, provider_name: str, file_object: File) -> FilePort:
        return self.providers[provider_name].generate_file(file_object)

    def get_file(self, provider_name: str, model_name: str, file_id: str) -> FilePort:
        return self.providers[provider_name].get_file(model_name, file_id)

    def generate_batch(
        self, provider_name: str, batch_request: BatchRequest
    ) -> BatchPort:
        return self.providers[provider_name].generate_batch(batch_request)

    def get_batch(
        self, provider_name: str, model_name: str, batch_id: str
    ) -> BatchPort:
        return self.providers[provider_name].get_batch(model_name, batch_id)
