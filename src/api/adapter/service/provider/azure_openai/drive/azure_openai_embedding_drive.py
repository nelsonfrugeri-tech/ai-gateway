from src.api.adapter.service.provider.port.embedding_port import EmbeddingPort
from src.api.adapter.service.provider.azure_openai.domain.embedding import Embedding
from src.api.adapter.service.provider.azure_openai.client.azure_openai_client import (
    AzureOpenAIClient,
)

from src.api.adapter.http.v1.payload.response.embedding_response import (
    EmbeddingResponse,
)
from src.api.adapter.http.v1.payload.request.embedding_request import EmbeddingRequest


class AzureOpenAIEmbeddingDrive(EmbeddingPort):
    def __init__(self, client: "AzureOpenAIClient"):
        self.client = client

    def generate(self, embedding_request: EmbeddingRequest) -> EmbeddingResponse:
        # FIXME check if the input is text, image or another type
        embedding = Embedding(
            input=embedding_request.content.texts,
            model=embedding_request.provider.model.name,
        )
        response = self.client.embedding(embedding)

        return EmbeddingResponse(
            data=[data.embedding for data in response.data],
            usage=response.usage,
        )
