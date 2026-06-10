from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.enums import Priority, Status


class ContactResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    name: str | None
    company: str | None
    created_at: datetime


class ClassificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email_id: int
    category: str
    sentiment: str | None
    urgency: str | None
    confidence: float | None


class EmailCreate(BaseModel):
    contact_email: EmailStr = Field(
        examples=["customer@example.com"],
    )
    contact_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        examples=["Asha Mehta"],
    )
    company: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
        examples=["Acme Corp"],
    )
    thread_identifier: str = Field(
        min_length=1,
        max_length=255,
        examples=["gmail-thread-123"],
    )
    message_identifier: str = Field(
        min_length=1,
        max_length=255,
        examples=["message-abc-001"],
    )
    sender: EmailStr = Field(
        examples=["customer@example.com"],
    )
    subject: str | None = Field(
        default=None,
        max_length=500,
        examples=["Urgent refund request"],
    )
    body: str = Field(
        min_length=1,
        examples=["This is urgent. I need a refund for my latest invoice."],
    )
    received_at: datetime = Field(
        examples=["2026-06-10T10:30:00Z"],
    )


class EmailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    thread_id: int
    message_identifier: str
    sender: str
    subject: str | None
    body: str
    received_at: datetime
    created_at: datetime
    classification: ClassificationResponse | None = None


class ThreadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    thread_identifier: str
    contact_id: int
    status: Status
    priority: Priority
    created_at: datetime


class AuditResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    event: str
    details: str | None
    email_id: int | None
    created_at: datetime
