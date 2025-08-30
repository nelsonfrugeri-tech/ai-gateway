from typing import List
from pydantic import field_validator
from src.api.adapter.http.v1.payload.common.base_payload import BasePayload
from src.api.adapter.http.v1.payload.request.common_request import Provider
from src.api.adapter.validation.model_validation import ModelValidation
from src.api.domain.provider import GenerationType


class Content(BasePayload):
    texts: List[str]


class EmbeddingRequest(BasePayload):
    content: Content
    provider: Provider

    @field_validator("provider", mode="after")
    def is_valid_embedding_model(cls, value):
        ModelValidation.validate_model_by_typel(
            model_name=value.model.name, generation_type=GenerationType.embedding
        )
        return value
