import json
from typing import AsyncGenerator, Optional
from src.api.adapter.service.provider.port.chat_port import ChatPort
from src.api.adapter.http.v1.payload.request.chat_request import (
    Message as MessageRequest,
    ChatRequest,
)
from src.api.adapter.http.v1.payload.response.chat_response import (
    ChatResponse,
    ChatStreamResponse,
    Tool as ToolResponse,
    Message,
    MessageStreamResponse,
    Usage,
)
from src.api.adapter.service.provider.azure_openai.domain.chat_completion import (
    ChatCompletion,
    Tool as ToolRequest,
    Message as ChatCompletionMessage,
    ToolMessage,
    Function,
    Parameters,
    Properties,
    ContentType,
    ImageUrl,
)
from src.api.adapter.http.v1.payload.response.guardrail_response import (
    GuardrailResponse,
)
from src.api.adapter.service.provider.azure_openai.client.azure_openai_client import (
    AzureOpenAIClient,
)

from src.api.core.cost.cost_client import CostClient, CostType


class AzureOpenAIChatDrive(ChatPort):

    def __init__(self, client: AzureOpenAIClient):
        self.client = client
        self.cost_client = CostClient()

    def generate(self, chat_request: ChatRequest) -> ChatResponse:
        chat_completion = ChatCompletion(
            model=chat_request.provider.model.name,
            messages=[
                self._set_tool_message(msg) for msg in chat_request.prompt.messages
            ],
            response_format=(
                {"type": "json_object"}
                if chat_request.prompt.parameter.json_mode
                else {"type": "text"}
            ),
        )
        self._set_parameters(chat_request=chat_request, chat_completion=chat_completion)

        self._set_tools(chat_request=chat_request, chat_completion=chat_completion)

        response = self.client.chat_completion(chat_completion)
        chat_response = (
            self._response_message_with_tools(
                response=response, tool_calls=response.choices[0].message.tool_calls
            )
            if response.choices[0].message.tool_calls is not None
            else self.__response_message(response)
        )

        chat_response.cost = self.cost_client.add(
            model_name=chat_request.provider.model.name,
            usage=chat_response.usage,
            cost_type=CostType.TEXT,
        )

        return chat_response

    async def generate_stream(
        self, chat_request: ChatRequest
    ) -> AsyncGenerator[ChatStreamResponse, None]:

        chat_completion = ChatCompletion(
            model=chat_request.provider.model.name,
            messages=[
                self._set_tool_message(msg) for msg in chat_request.prompt.messages
            ],
            stream=True,
            n=1,
            stream_options={"include_usage": True},
        )

        self._set_parameters(chat_request=chat_request, chat_completion=chat_completion)

        stream = self.client.chat_completion(chat_completion)

        for chunk in stream:
            response = await self.__extract_response_from_chunk(
                chat_request.provider.model.name, chunk
            )

            if response is not None:
                yield response.model_dump_json(exclude_none=True)

    def _set_parameters(
        self, chat_request: ChatRequest, chat_completion: ChatCompletion
    ) -> None:

        if chat_request.prompt.parameter is not None:
            chat_completion.set_temperature(
                temperature=chat_request.prompt.parameter.temperature
            )
            chat_completion.set_max_tokens(
                max_tokens=chat_request.prompt.parameter.max_tokens
            )

    def _set_tools(
        self, chat_request: ChatRequest, chat_completion: ChatCompletion
    ) -> None:

        tools = []
        if chat_request.tools is not None:
            for tool in chat_request.tools:

                properties = {}
                if tool.parameters is not None:
                    for key, property in tool.parameters.properties.items():
                        properties[key] = Properties(
                            type=property.type,
                            description=property.description,
                            enum=(property.enum if property.enum else []),
                        )

                tools.append(
                    ToolRequest(
                        function=Function(
                            name=tool.name,
                            description=tool.description,
                            parameters=Parameters(
                                type=tool.parameters.type,
                                properties=properties,
                                required=(
                                    tool.parameters.required
                                    if tool.parameters.required
                                    else []
                                ),
                            ),
                        )
                    )
                )

        chat_completion.set_tools(tools=tools, tool_choice=chat_request.tool_choice)

    def _response_message_with_tools(
        self, response: dict, tool_calls: list
    ) -> ChatResponse:

        messages = []

        for tool in tool_calls:
            tool = ToolResponse(
                id=tool.id,
                name=tool.function.name,
                arguments=json.loads(tool.function.arguments),
            )

            message = Message(role="tool", tool=tool)

            messages.append(message)

        return ChatResponse(
            usage=Usage(
                completionTokens=response.usage.completion_tokens,
                promptTokens=response.usage.prompt_tokens,
                totalTokens=response.usage.total_tokens,
            ),
            messages=messages,
        )

    def _set_tool_message(self, message: MessageRequest) -> dict:
        return (
            ToolMessage(
                tool_call_id=message.tool.id,
                role=message.role,
                name=message.tool.name,
                content=message.content,
            )
            if message.role == "function"
            else self._set_message(message)
        )

    def _set_message(self, message: MessageRequest) -> ChatCompletionMessage:
        return (
            ChatCompletionMessage(
                role=message.role,
                content=[
                    ContentType(
                        type=content.type,
                        text=content.text if content.type == "text" else None,
                        image_url=(
                            ImageUrl(url=content.image_url.url)
                            if content.type == "image_url"
                            else None
                        ),
                        detail=content.detail or None,
                    )
                    for content in message.content
                ],
            )
            if message.content is not None and isinstance(message.content, list)
            else ChatCompletionMessage(role=message.role, content=message.content)
        )

    def __response_message(self, response: dict) -> ChatResponse:
        return ChatResponse(
            usage=Usage(
                completionTokens=response.usage.completion_tokens,
                promptTokens=response.usage.prompt_tokens,
                totalTokens=response.usage.total_tokens,
            ),
            messages=[
                Message(
                    role=response.choices[0].message.role,
                    content=response.choices[0].message.content,
                )
            ],
            guardrail=GuardrailResponse.from_filter_results(
                completion_filter_results=(
                    response.choices[0].content_filter_results
                    if hasattr(response.choices[0], "content_filter_results")
                    else None
                ),
                prompt_filter_results=(
                    response.prompt_filter_results[0].get("content_filter_result")
                    or response.prompt_filter_results[0].get("content_filter_results")
                    if hasattr(response, "prompt_filter_results")
                    and (
                        "content_filter_result" in response.prompt_filter_results[0]
                        or "content_filter_results" in response.prompt_filter_results[0]
                    )
                    else None
                ),
            ),
        )

    async def __get_messages_stream(
        self, content: str = None, role: str = None
    ) -> MessageStreamResponse:
        return MessageStreamResponse(
            content=content,
            role=role,
        )

    async def __get_completion_filter_stream(
        self, content_filter_results
    ) -> GuardrailResponse:
        return GuardrailResponse.from_filter_results(
            completion_filter_results=content_filter_results
        )

    async def __get_prompt_filter_stream(
        self, prompt_filter_result
    ) -> GuardrailResponse:
        return GuardrailResponse.from_filter_results(
            prompt_filter_results=(
                prompt_filter_result.get("content_filter_result")
                or prompt_filter_result.get("content_filter_results")
                if "content_filter_result" in prompt_filter_result
                or "content_filter_results" in prompt_filter_result
                else None
            )
        )

    async def __response_chat_stream_message(
        self,
        message: MessageStreamResponse = None,
        guardrail: GuardrailResponse = None,
        usage: Usage = None,
    ) -> ChatStreamResponse:
        return ChatStreamResponse(message=message, guardrail=guardrail, usage=usage)

    async def __extract_response_from_chunk(
        self, model: str, chunk
    ) -> Optional[ChatStreamResponse]:
        if chunk.choices:
            choice = chunk.choices[0]
            if hasattr(choice, "delta") and choice.delta:
                if choice.delta.content is None and choice.delta.role is None:
                    return None
                return await self.__response_chat_stream_message(
                    message=await self.__get_messages_stream(
                        content=choice.delta.content, role=choice.delta.role
                    )
                )
            elif (
                hasattr(choice, "content_filter_results")
                and choice.content_filter_results
            ):
                return await self.__response_chat_stream_message(
                    guardrail=await self.__get_completion_filter_stream(
                        chunk.choices[0].content_filter_results
                    )
                )
        elif hasattr(chunk, "prompt_filter_results") and chunk.prompt_filter_results:
            return await self.__response_chat_stream_message(
                guardrail=await self.__get_prompt_filter_stream(
                    chunk.prompt_filter_results[0]
                )
            )
        elif hasattr(chunk, "usage") and chunk.usage is not None:
            chat_stream_response = await self.__response_chat_stream_message(
                usage=chunk.usage
            )
            chat_stream_response.cost = self.cost_client.add(
                model_name=model,
                usage=chat_stream_response.usage,
                cost_type=CostType.TEXT,
            )
            return chat_stream_response
        return None
