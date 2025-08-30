from pydantic import BaseModel, field_validator
from typing import Optional
from src.api.core.exception.bad_request_exception import (
    BadRequestException,
)
from typing_extensions import Literal

from src.api.domain.provider import GenerationType
from .common_request import Provider
from src.api.adapter.validation.model_validation import ModelValidation


class PromptParameter(BaseModel):
    n: Optional[int] = None
    quality: Literal["standard", "hd"] = None
    response_format: Optional[Literal["url", "b64_json"]] = None
    size: Optional[str] = None
    style: Optional[Literal["vivid", "natural"]] = None


class Prompt(BaseModel):
    message: str
    parameter: Optional[PromptParameter] = None


class ImageRequest(BaseModel):
    provider: Provider
    prompt: Prompt

    @classmethod
    def validate(
        cls,
        provider: Provider,
        prompt: Prompt,
    ) -> "ImageRequest":
        model_name = provider.model.name
        size = prompt.parameter.size

        if model_name.startswith("dall-e-3") and prompt.parameter.n != 1:
            raise BadRequestException(params=["For dall-e-3, only n=1 is supported."])

        cls.validate_size(model_name, size)

        return cls(
            provider=provider,
            prompt=prompt,
        )

    @classmethod
    def validate_size(cls, model_name: str, size: str):
        if model_name.startswith("dall-e-3"):
            valid_sizes = ["1024x1024", "1792x1024", "1024x1792"]
        else:
            valid_sizes = ["256x256", "512x512", "1024x1024"]

        if size not in valid_sizes:
            raise BadRequestException(
                params=[
                    f"Size '{size}' is not valid for {model_name}. Valid sizes are {valid_sizes}"
                ]
            )

    @field_validator("provider", mode="after")
    def is_valid_image_model(cls, value):
        ModelValidation.validate_model_by_typel(
            model_name=value.model.name, generation_type=GenerationType.image
        )
        return value
