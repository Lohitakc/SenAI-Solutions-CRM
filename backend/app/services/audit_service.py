import logging

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.repositories.audit_repository import AuditRepository

logger = logging.getLogger(__name__)


class AuditService:
    def __init__(self, db: Session) -> None:
        self.repository = AuditRepository(db)

    def log_event(self, event: str, details: str | None, email_id: int | None = None) -> AuditLog:
        logger.info("Writing audit event: %s", event)
        return self.repository.create(event=event, details=details, email_id=email_id)
