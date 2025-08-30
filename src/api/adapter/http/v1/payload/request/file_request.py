import base64
from enum import Enum
from pydantic import field_validator, ConfigDict
from src.api.adapter.http.v1.payload.common.base_payload import BasePayload
from src.api.adapter.http.v1.payload.request.common_request import Provider
from src.api.adapter.validation.model_validation import ModelValidation


class FileExtensionTypeRequest(Enum):
    JSONL = "jsonl"


class FilePurposeRequestName(Enum):
    BATCH = "batch"


class FileExtensionRequest(BasePayload):
    name: FileExtensionTypeRequest


class FilePurposeRequest(BasePayload):
    name: FilePurposeRequestName


class FileEndpointNameRequest(str, Enum):
    CHAT: str = "/chat/completions"


class FileEndpointRequest(BasePayload):
    name: FileEndpointNameRequest


class FileRequest(BasePayload):
    provider: Provider
    endpoint: FileEndpointRequest
    content: str
    name: str
    extension: FileExtensionRequest
    purpose: FilePurposeRequest
    model_config = ConfigDict(use_enum_values=True)

    @field_validator("content", mode="after")
    def is_valid_base64(cls, value: str) -> str:
        try:
            base64.b64decode(value, validate=True)
        except Exception:
            raise ValueError("Invalid Base64 string")
        return value

    @field_validator("purpose", mode="after")
    def is_valid_purpose(cls, value: FilePurposeRequest, values: dict):
        provider: Provider = values.data.get("provider")
        ModelValidation.validate_batch_purpose(
            purpose_name=value.name.value, model_name=provider.model.name
        )

        return value
