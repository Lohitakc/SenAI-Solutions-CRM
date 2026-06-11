from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import Priority, Status
from app.schemas.email import ClassificationResponse


class InboxEmailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    thread_id: int
    sender: str
    subject: str | None
    received_at: datetime
    priority: Priority
    status: Status
    category: str | None


class ThreadDetailResponse(BaseModel):
    id: int
    thread_identifier: str
    contact_id: int
    status: Status
    priority: Priority
    emails: list[dict]


class MetricPoint(BaseModel):
    name: str
    value: int


class DashboardSummaryResponse(BaseModel):
    total_emails: int
    open_threads: int
    escalations: int
    average_response_time: str
    sentiment_distribution: list[MetricPoint]
    category_distribution: list[MetricPoint]
    priority_distribution: list[MetricPoint]
    daily_volume: list[MetricPoint]
    human_intervention_rate: float
    recent_activity: list[dict]
