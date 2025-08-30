import numpy as np

from abc import ABC, abstractmethod
from src.api.adapter.http.v1.payload.request.similarity_request import (
    SimilarityRequest,
    MetricType,
)
from src.api.adapter.http.v1.payload.response.similarity_response import (
    SimilarityResponse,
    ResultResponse,
)

from src.api.adapter.http.v1.payload.response.embedding_response import (
    EmbeddingResponse,
)

from src.api.adapter.http.v1.payload.request.embedding_request import (
    EmbeddingRequest,
    Content,
)

from src.api.adapter.service.provider.service_provider import ServiceProvider

from src.api.core.business.embedding_business import EmbeddingBusiness


class SimilarityBusiness:

    def __init__(self):
        self.service_provider = ServiceProvider()
        self.embedding_business = EmbeddingBusiness()

    def generate_similarity(self, similarity_request: SimilarityRequest):
        embedding_response = self.__get_embedding_response(similarity_request)
        embeddings = embedding_response.data

        return SimilarityResponse(
            results=[
                ResultResponse(
                    embedding=embedding, text=similarity_request.evaluation.texts[idx]
                )
                for idx, embedding in enumerate(embeddings)
            ],
            score=EvaluationSimilarity.evaluate(
                similarity_request.evaluation.metric_type
            ).calculate(embeddings[0], embeddings[1]),
            usage=embedding_response.usage,
            cost=embedding_response.cost,
        )

    def __get_embedding_response(
        self, similarity_request: SimilarityRequest
    ) -> EmbeddingResponse:
        return self.embedding_business.generate_embedding(
            embedding_request=EmbeddingRequest(
                content=Content(texts=similarity_request.evaluation.texts),
                provider=similarity_request.provider,
            )
        )


class InterfaceSimilarity(ABC):
    @abstractmethod
    def calculate(self, embedding1, embedding2):
        pass


class CosineSimilarity(InterfaceSimilarity):
    def calculate(self, embedding1, embedding2):
        dot_product = np.dot(embedding1, embedding2)
        norm_a = np.linalg.norm(embedding1)
        norm_b = np.linalg.norm(embedding2)
        return dot_product / (norm_a * norm_b)


class EuclideanSimilarity(InterfaceSimilarity):
    def calculate(self, embedding1, embedding2):
        return np.linalg.norm(np.array(embedding1) - np.array(embedding2))


class ManhattanSimilarity(InterfaceSimilarity):
    def calculate(self, embedding1, embedding2):
        return np.sum(np.abs(np.array(embedding1) - np.array(embedding2)))


class EvaluationSimilarity:
    @staticmethod
    def evaluate(metric_type: MetricType) -> InterfaceSimilarity:
        evaluation = {
            MetricType.COSINE: CosineSimilarity(),
            MetricType.EUCLIDEAN: EuclideanSimilarity(),
            MetricType.MANHATTAN: ManhattanSimilarity(),
        }
        return evaluation.get(metric_type)
