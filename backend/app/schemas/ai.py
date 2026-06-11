from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RagSearchRequest(BaseModel):
    query: str = Field(min_length=1, examples=["What is the refund policy for urgent billing disputes?"])
    top_k: int = Field(default=3, ge=1, le=10)
    threshold: float = Field(default=0.0, ge=0.0, le=1.0)


class RetrievedChunkResponse(BaseModel):
    content: str
    title: str | None
    source_file: str | None
    score: float
    embedding_reference: str | None


class RagSearchResponse(BaseModel):
    query: str
    chunks: list[RetrievedChunkResponse]


class AIEmailRequest(BaseModel):
    sender: EmailStr = Field(examples=["customer@example.com"])
    subject: str | None = Field(default=None, examples=["Urgent refund complaint"])
    body: str = Field(min_length=1, examples=["This is urgent. I need a refund and may escalate legally."])
    thread_history: list[str] = Field(default_factory=list)
    email_id: int | None = None


class AIClassificationResponse(BaseModel):
    category: str
    sentiment: str | None
    urgency: str | None
    confidence: float
    human_required: bool
    summary: str
    reply_draft: str
    retrieved_chunks: list[RetrievedChunkResponse]


class ReplyResponse(BaseModel):
    reply_draft: str
    retrieved_chunks: list[RetrievedChunkResponse]


class AgentAnalyzeResponse(BaseModel):
    reasoning_id: int
    reasoning: str
    classification: AIClassificationResponse
    execution_plan: list[str]
    escalation_required: bool
    status: str


class AgentHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email_id: int | None
    reasoning: str
    retrieved_chunks: str
    prompt_metadata: str
    classification: str
    reply_draft: str
    execution_plan: str
    status: str
    created_at: datetime
