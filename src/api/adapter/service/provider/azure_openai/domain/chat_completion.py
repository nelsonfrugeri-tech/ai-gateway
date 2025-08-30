import base64

from urllib.parse import urlparse
from pydantic import BaseModel, field_validator, Field
from typing import List, Optional, Dict, Union
from src.api.adapter.http.v1.payload.request.chat_request import ToolChoice
from src.api.core.exception.bad_request_exception import (
    BadRequestException,
)
from typing import Literal

from src.api.core.exception.internal_server_error_exception import (
    InternalServerErrorException,
)
from src.api.adapter.constant.base64_constant import Extension
from src.api.adapter.constant.chat_completion import MessageRole


class ToolMessage(BaseModel):
    tool_call_id: str
    role: str
    name: str
    content: str


class ImageUrl(BaseModel):
    url: str

    @classmethod
    def get_image_extension(cls, value: str) -> str:
        data: bytes = base64.b64decode(value, validate=True)

        if data.startswith(Extension.JPEG.value):
            return "jpeg"
        elif data.startswith(Extension.PNG.value):
            return "png"
        elif data.startswith(Extension.GIF87A.value) or data.startswith(
            Extension.GIF89A.value
        ):
            return "gif"
        elif (
            data.startswith(Extension.WEBP.value)
            and data[8:12] == Extension.WEBP_SUBSTRING.value
        ):
            return "webp"
        else:
            raise InternalServerErrorException()

    @field_validator("url")
    def validate_and_convert_url(cls, value):
        try:
            parsed_url = urlparse(value)
            if parsed_url.scheme and parsed_url.netloc:
                return value
            else:
                return f"data:image/{cls.get_image_extension(value)};base64,{value}"
        except (TypeError, ValueError):
            raise InternalServerErrorException()


class ContentType(BaseModel):
    type: str
    text: Optional[str] = None
    image_url: Optional[ImageUrl] = None
    detail: Optional[str] = None


class Message(BaseModel):
    role: str
    content: Union[str, List[ContentType]]


class Properties(BaseModel):
    type: str
    description: Optional[str] = None
    enum: Optional[List[str]] = Field(default_factory=list)


class Parameters(BaseModel):
    type: str
    properties: Dict[str, Properties]
    required: Optional[List[str]] = Field(default_factory=list)


class Function(BaseModel):
    name: str
    description: str
    parameters: Optional[Parameters] = None


class Tool(BaseModel):
    type: str = "function"
    function: Function


class ChatCompletion(BaseModel):
    model: str
    messages: List[Union[Message, ToolMessage]] = []
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    n: Optional[int] = None
    stop: Optional[List[str]] = None
    tools: Optional[List[Tool]] = None
    tool_choice: Optional[Union[ToolChoice, str]] = None
    response_format: Dict[str, Literal["json_object", "text"]] = Field(
        default={"type": "text"}
    )
    stream: Optional[bool] = None
    stream_options: Optional[dict] = None

    @field_validator("temperature", "top_p")
    def check_probability(cls, value, ctx):
        if value is not None and (value < 0.0 or value > 1.0):
            raise BadRequestException(
                params=[f"The {ctx.field_name} field must be between 0 and 1"]
            )
        return value

    @field_validator("messages")
    def validate_roles(cls, messages):
        for message in messages:
            if not MessageRole.is_valid(message.role):
                roles = MessageRole.get_roles()
                raise BadRequestException(
                    params=[
                        f"Invalid {message.role} role! The valid roles are {*roles,}"
                    ]
                )
        return messages

    def set_temperature(self, temperature: float) -> None:
        if temperature is not None:
            self.temperature = temperature

    def set_max_tokens(self, max_tokens: int) -> None:
        if max_tokens is not None:
            self.max_tokens = max_tokens

    def set_tools(self, tools: List[Tool], tool_choice: Union[str, ToolChoice]) -> None:
        if len(tools) > 0:
            self.tools = tools

            self.tool_choice = tool_choice if tool_choice is not None else "auto"
