import tiktoken

from src.api.adapter.http.v1.payload.request.embedding_request import EmbeddingRequest

from src.api.adapter.service.provider.port.embedding_port import EmbeddingPort
from src.api.adapter.service.provider.service_provider import ServiceProvider
from src.api.core.cost.cost_client import CostClient, CostType
from src.api.adapter.cache.simple.provider_cache import ProviderCache

from src.api.core.exception.bad_request_exception import (
    BadRequestException,
)


class EmbeddingBusiness:

    def __init__(self):
        self.service_provider = ServiceProvider()
        self.cost_client = CostClient()

    def generate_embedding(self, embedding_request: EmbeddingRequest) -> EmbeddingPort:
        model_name = embedding_request.provider.model.name
        self.check_num_tokens_from_texts(model_name, embedding_request.content.texts)
        embedding_response = self.service_provider.generate_embedding(
            provider_name=embedding_request.provider.name,
            embedding_request=embedding_request,
        )
        embedding_response.cost = self.cost_client.add(
            model_name=model_name,
            usage=embedding_response.usage,
            cost_type=CostType.TEXT,
        )
        return embedding_response

    def check_num_tokens_from_texts(self, model_name: str, texts: list):
        encoding = tiktoken.encoding_for_model(model_name)
        max_input_model = ProviderCache.get_provider_model(model_name).max_input

        for text in texts:
            num_tokens = len(encoding.encode(text))
            self.__check_num_tokens(num_tokens, max_input_model)

    def __check_num_tokens(self, num_tokens: int, max_input_model: int):
        if num_tokens > max_input_model:
            raise BadRequestException(
                params=[
                    f"The number of the tokens in the text cannot be bigger than {max_input_model}"
                ]
            )
