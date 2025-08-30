from typing import AsyncGenerator
from src.api.adapter.service.provider.azure_openai.drive.azure_openai_chat_drive import (
    AzureOpenAIChatDrive,
)
from src.api.adapter.service.provider.azure_openai.drive.azure_openai_image_drive import (
    AzureOpenAIImageDrive,
)
from src.api.adapter.service.provider.azure_openai.drive.azure_openai_embedding_drive import (
    AzureOpenAIEmbeddingDrive,
)
from src.api.adapter.service.provider.azure_openai.drive.azure_openai_file_drive import (
    AzureOpenAIFileDrive,
)
from src.api.adapter.service.provider.azure_openai.drive.azure_openai_batch_drive import (
    AzureOpenAIBatchDrive,
)

from src.api.adapter.http.v1.payload.request.chat_request import (
    ChatRequest,
)
from src.api.adapter.http.v1.payload.response.chat_response import (
    ChatResponse,
    ChatStreamResponse,
)
from src.api.adapter.service.provider.azure_openai.client.azure_openai_client import (
    AzureOpenAIClient,
)
from src.api.adapter.http.v1.payload.request.image_request import ImageRequest
from src.api.adapter.http.v1.payload.response.image_response import ImageResponse

from src.api.adapter.http.v1.payload.response.embedding_response import (
    EmbeddingResponse,
)
from src.api.adapter.http.v1.payload.request.embedding_request import EmbeddingRequest

from src.api.adapter.http.v1.payload.response.file_response import (
    FileResponse,
)

from src.api.domain.file import File

from src.api.adapter.http.v1.payload.request.batch_request import BatchRequest
from src.api.adapter.http.v1.payload.response.batch_response import (
    BatchResponse,
)


class AzureOpenAIDrive:
    def __init__(self):
        self.client: AzureOpenAIClient = AzureOpenAIClient()
        self.chat_drive = AzureOpenAIChatDrive(self.client)
        self.image_drive = AzureOpenAIImageDrive(self.client)
        self.embedding_drive = AzureOpenAIEmbeddingDrive(self.client)
        self.file_drive = AzureOpenAIFileDrive(self.client)
        self.batch_drive = AzureOpenAIBatchDrive(self.client)

    def generate_text(self, chat_request: ChatRequest) -> ChatResponse:
        return self.chat_drive.generate(chat_request)

    def generate_text_stream(
        self, chat_request: ChatRequest
    ) -> AsyncGenerator[ChatStreamResponse, None]:
        return self.chat_drive.generate_stream(chat_request)

    def generate_image(self, image_request: ImageRequest) -> ImageResponse:
        return self.image_drive.generate(image_request)

    def generate_embedding(
        self, embedding_request: EmbeddingRequest
    ) -> EmbeddingResponse:
        return self.embedding_drive.generate(embedding_request)

    def generate_file(self, file_object: File) -> FileResponse:
        return self.file_drive.generate(file_object)

    def generate_batch(self, batch_request: BatchRequest) -> BatchResponse:
        return self.batch_drive.generate(batch_request)

    def get_file(self, model_name: str, file_id: File) -> FileResponse:
        return self.file_drive.get(model_name, file_id)

    def get_batch(self, model_name: str, batch_id: str) -> BatchResponse:
        return self.batch_drive.get(model_name, batch_id)
