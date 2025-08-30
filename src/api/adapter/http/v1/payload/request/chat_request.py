import base64
from urllib.parse import urlparse
from pydantic import BaseModel, field_validator
from typing import List, Dict, Optional, Union
from src.api.core.exception.bad_request_exception import (
    BadRequestException,
)
from src.api.core.exception.internal_server_error_exception import (
    InternalServerErrorException,
)
from src.api.adapter.cache.simple.provider_cache import ProviderCache
from src.api.domain.provider import GenerationType
from .common_request import Provider
from src.api.adapter.constant.base64_constant import Extension
from src.api.adapter.http.v1.payload.common.base_payload import BasePayload
from src.api.adapter.validation.model_validation import ModelValidation


class PromptParameter(BasePayload):
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    json_mode: Optional[bool] = None

    @field_validator("temperature")
    def validate_prompt(cls, value, context):
        if value is not None and (value < 0.0 or value > 1.0):
            raise BadRequestException(
                params=[f"The {context.field_name} field must be between 0 and 1"]
            )
        return value


class ToolMessage(BasePayload):
    id: str
    name: str
    arguments: Optional[str] = None


class ImageUrl(BaseModel):
    url: str

    @classmethod
    def validate_image_extension(cls, value: str) -> str:
        try:
            data: bytes = base64.b64decode(value, validate=True)

            if data.startswith(Extension.JPEG.value):
                return value
            elif data.startswith(Extension.PNG.value):
                return value
            elif data.startswith(Extension.GIF87A.value) or data.startswith(
                Extension.GIF89A.value
            ):
                return value
            elif (
                data.startswith(Extension.WEBP.value)
                and data[8:12] == Extension.WEBP_SUBSTRING.value
            ):
                return value
            else:
                raise BadRequestException(
                    params=[f"url field must be a valid URL or base64"]
                )
        except (TypeError, ValueError):
            raise BadRequestException(
                params=[f"url field must be a valid URL or base64"]
            )

    @field_validator("url")
    def validate_url_or_base64(cls, value: str) -> str:
        try:
            parsed_url = urlparse(value)
            if parsed_url.scheme and parsed_url.netloc:
                return value

            return cls.validate_image_extension(value)
        except Exception:
            raise BadRequestException(
                params=[f"url field must be a valid URL or base64"]
            )


class ContentType(BasePayload):
    type: str
    text: Optional[str] = None
    image_url: Optional[ImageUrl] = None
    detail: Optional[str] = None


class Message(BasePayload):
    role: str
    content: Union[str, List[ContentType]]
    tool: Optional[ToolMessage] = None


class Prompt(BasePayload):
    parameter: Optional[PromptParameter] = None
    messages: List[Message]


class Properties(BasePayload):
    type: str
    description: Optional[str] = None
    enum: Optional[list] = None


class ToolParameter(BasePayload):
    type: str
    properties: Dict[str, Properties]
    required: Optional[List[str]] = None


class Tool(BasePayload):
    name: str
    description: str
    parameters: Optional[ToolParameter]


class FunctionSpecification(BasePayload):
    name: str


class ToolChoice(BasePayload):
    type: str
    function: Optional[FunctionSpecification] = None


class ChatRequest(BasePayload):
    provider: Provider
    prompt: Prompt
    tools: Optional[List[Tool]] = None
    tool_choice: Optional[Union[str, ToolChoice]] = None

    @classmethod
    def validate(
        cls,
        provider: Provider,
        prompt: Prompt,
        tools: Optional[List[Tool]] = None,
        toolChoice: Optional[Union[str, ToolChoice]] = None,
    ) -> "ChatRequest":
        try:
            model_name = provider.model.name
            max_tokens = prompt.parameter.max_tokens
            context_window = ProviderCache.get_context_window_for_model(
                model_name=model_name
            )

            cls.validate_tool(toolChoice, tools)

            ModelValidation.validate_model_by_typel(
                model_name=model_name, generation_type=GenerationType.text
            )

            ModelValidation.validate_max_tokens(
                max_tokens=max_tokens,
                context_window=context_window,
                model_name=model_name,
            )

            return cls(
                provider=provider,
                prompt=prompt,
                tools=tools,
                toolChoice=toolChoice,
            )
        except Exception as exception:
            raise InternalServerErrorException(
                exception=exception, message="Error on the chat request validation!"
            )

    @classmethod
    def validate_tool(
        cls,
        toolChoice: Optional[Union[str, ToolChoice]] = None,
        tools: Optional[List[Tool]] = None,
    ):
        try:
            if toolChoice is not None:
                if isinstance(toolChoice, str):
                    if toolChoice not in ["required", "auto", "none"]:
                        raise BadRequestException(
                            params=[
                                "toolChoice must be 'required', 'auto', 'none', or a valid function specification."
                            ]
                        )
                elif isinstance(toolChoice, ToolChoice):
                    if toolChoice.function and toolChoice.type == "function":
                        function_name = toolChoice.function.name
                        if not any(tool.name == function_name for tool in tools):
                            raise BadRequestException(
                                params=[
                                    f"Function name '{function_name}' not found in the provided tools."
                                ]
                            )
        except Exception as exception:
            raise InternalServerErrorException(
                exception=exception, message="Validate Tool Error!"
            )
