from enum import Enum
from pydantic import field_validator
from typing import List, Optional
from src.api.core.exception.bad_request_exception import BadRequestException
from src.api.adapter.http.v1.payload.common.base_payload import BasePayload
from src.api.adapter.http.v1.payload.request.common_request import Provider
from src.api.adapter.validation.model_validation import ModelValidation
from src.api.domain.provider import GenerationType


class MetricType(Enum):
    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    MANHATTAN = "manhattan"


class EvaluationRequest(BasePayload):
    texts: List[str]
    metric_type: Optional[MetricType] = MetricType.COSINE

    @field_validator("texts")
    def validate_texts_size(cls, value):
        if len(value) != 2:
            raise BadRequestException(
                params=[
                    "Ensure that you provided two texts to compare the similarity between each other!"
                ]
            )
        return value


class SimilarityRequest(BasePayload):
    provider: Provider
    evaluation: EvaluationRequest

    @field_validator("provider", mode="after")
    def is_valid_embedding_model(cls, value):
        ModelValidation.validate_model_by_typel(
            model_name=value.model.name, generation_type=GenerationType.embedding
        )
        return value
