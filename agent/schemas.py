from typing import Any

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    conversation_id: str
    role: str
    content: str | list[dict[str, Any]]


class StreamEvent(BaseModel):
    step: str
    content: str | list[dict[str, Any]]
