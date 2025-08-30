from typing import List, Optional
from src.api.adapter.http.v1.payload.common.base_payload import BasePayload
from src.api.adapter.http.v1.payload.response.cost_response import Cost, Usage
from src.api.adapter.http.v1.payload.response.guardrail_response import (
    GuardrailResponse,
)


class Tool(BasePayload):
    id: str
    name: str
    arguments: dict


class Message(BasePayload):
    role: str
    content: Optional[str] = None
    tool: Optional[Tool] = None


class ChatResponse(BasePayload):
    usage: Optional[Usage] = None
    cost: Optional[Cost] = None
    messages: List[Message]
    guardrail: Optional[GuardrailResponse] = None


class MessageStreamResponse(BasePayload):
    role: Optional[str] = None
    content: Optional[str] = None


class ChatStreamResponse(BasePayload):
    usage: Optional[Usage] = None
    cost: Optional[Cost] = None
    message: Optional[MessageStreamResponse] = None
    guardrail: Optional[GuardrailResponse] = None
