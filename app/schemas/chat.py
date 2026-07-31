from datetime import datetime

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2_000)
    conversation_id: str | None = None
    channel: str = Field(default="text", pattern="^(text|voice)$")


class ToolExecution(BaseModel):
    name: str
    arguments: dict
    result_summary: str


class Citation(BaseModel):
    title: str
    source: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    conversation_id: str
    provider: str
    intent: str
    state: str
    trace_id: str
    tools_used: list[ToolExecution] = []
    citations: list[Citation] = []


class MessageRead(BaseModel):
    role: str
    content: str
    intent: str | None
    tool_name: str | None
    created_at: datetime


class ConversationRead(BaseModel):
    id: str
    status: str
    channel: str
    last_intent: str | None
    messages: list[MessageRead]


class HandoffCreate(BaseModel):
    conversation_id: str
    reason: str = Field(min_length=3, max_length=500)


class HandoffRead(BaseModel):
    id: int
    conversation_id: str
    reason: str
    status: str


class FeedbackCreate(BaseModel):
    conversation_id: str
    rating: int = Field(ge=1, le=5)
    comment: str | None = Field(default=None, max_length=1_000)


class FeedbackRead(BaseModel):
    id: int
    conversation_id: str
    rating: int
    comment: str | None


class RealtimeTokenRequest(BaseModel):
    user_id: str = Field(min_length=3, max_length=100)


class RealtimeToolRequest(BaseModel):
    conversation_id: str | None = None
    name: str = Field(min_length=1, max_length=100)
    arguments: dict


class RealtimeToolResponse(BaseModel):
    conversation_id: str
    output: dict
