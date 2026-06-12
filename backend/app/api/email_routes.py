from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.email import AssessmentEmailCreate, ContactResponse, EmailCreate, EmailResponse, ThreadResponse
from app.schemas.dashboard import DashboardSummaryResponse, InboxEmailResponse, ThreadDetailResponse
from app.services.database_health_service import DatabaseHealthService
from app.services.dashboard_service import DashboardService
from app.services.email_service import EmailService
from app.services.action_service import ActionService
from app.services.query_service import QueryService

router = APIRouter()


@router.post(
    "/emails/ingest",
    response_model=EmailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Ingest an email",
)
def ingest_email(payload: EmailCreate, db: Session = Depends(get_db)) -> EmailResponse:
    email = EmailService(db).ingest_email(payload)
    return EmailResponse.model_validate(email)


@router.post(
    "/ingest",
    response_model=EmailResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Ingest an assessment-compatible email payload",
)
def ingest_assessment_email(payload: AssessmentEmailCreate, db: Session = Depends(get_db)) -> EmailResponse:
    email = EmailService(db).ingest_assessment_record(payload.model_dump())
    return EmailResponse.model_validate(email)


@router.post(
    "/ingest/replay",
    summary="Replay the provided assessment dataset",
)
def replay_assessment_dataset(
    limit: int | None = None,
    delay_seconds: float = 0.0,
    db: Session = Depends(get_db),
) -> dict[str, int]:
    return EmailService(db).replay_assessment_dataset(limit=limit, delay_seconds=delay_seconds)


@router.get(
    "/emails",
    response_model=list[InboxEmailResponse],
    summary="List ingested emails for inbox views",
)
def list_emails(
    search: str | None = None,
    priority: str | None = None,
    status: str | None = None,
    limit: int = 25,
    offset: int = 0,
    sort: str = "received_at_desc",
    db: Session = Depends(get_db),
) -> list[InboxEmailResponse]:
    return DashboardService(db).list_inbox(search, priority, status, limit, offset, sort)


@router.get(
    "/emails/{email_id}",
    response_model=EmailResponse,
    summary="Get an email by ID",
)
def get_email(email_id: int, db: Session = Depends(get_db)) -> EmailResponse:
    email = EmailService(db).get_email(email_id)
    return EmailResponse.model_validate(email)


@router.get(
    "/threads/{thread_id}",
    response_model=ThreadResponse,
    summary="Get a thread by ID",
)
def get_thread(thread_id: int, db: Session = Depends(get_db)) -> ThreadResponse:
    thread = QueryService(db).get_thread(thread_id)
    return ThreadResponse.model_validate(thread)


@router.get(
    "/threads/{thread_id}/detail",
    response_model=ThreadDetailResponse,
    summary="Get a full thread detail view",
)
def get_thread_detail(thread_id: int, db: Session = Depends(get_db)) -> ThreadDetailResponse:
    return DashboardService(db).get_thread_detail(thread_id)


@router.get(
    "/customers",
    summary="List enriched customer profiles",
)
def list_customers(db: Session = Depends(get_db)) -> list[dict]:
    return QueryService(db).list_customer_profiles()


@router.get(
    "/customers/{contact_id}",
    summary="Get enriched customer profile",
)
def get_customer_profile(contact_id: int, db: Session = Depends(get_db)) -> dict:
    return QueryService(db).get_customer_profile(contact_id)


@router.get(
    "/contacts/{contact_id}",
    response_model=ContactResponse,
    summary="Get a contact by ID",
)
def get_contact(contact_id: int, db: Session = Depends(get_db)) -> ContactResponse:
    contact = QueryService(db).get_contact(contact_id)
    return ContactResponse.model_validate(contact)


@router.get(
    "/health/database",
    summary="Check database health",
)
def database_health(db: Session = Depends(get_db)) -> dict[str, str]:
    return DatabaseHealthService(db).check()


@router.get(
    "/analytics/summary",
    response_model=DashboardSummaryResponse,
    summary="Get dashboard and analytics summary",
)
def analytics_summary(db: Session = Depends(get_db)) -> DashboardSummaryResponse:
    return DashboardService(db).summary()


@router.post(
    "/emails/{email_id}/approve-reply",
    summary="Approve a drafted reply recommendation",
)
def approve_reply(
    email_id: int,
    payload: dict | None = Body(default=None),
    db: Session = Depends(get_db),
) -> dict[str, str]:
    edited_draft = payload.get("edited_draft") if payload else None
    return ActionService(db).approve_reply(email_id, edited_draft)


@router.post(
    "/threads/{thread_id}/escalate",
    summary="Escalate a thread for human review",
)
def escalate_thread(thread_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    return ActionService(db).escalate_thread(thread_id)
