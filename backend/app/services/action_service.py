from sqlalchemy.orm import Session

from app.models.enums import Priority, Status
from app.repositories.action_repository import ActionRepository
from app.repositories.email_repository import EmailRepository
from app.repositories.thread_repository import ThreadRepository
from app.services.audit_service import AuditService
from app.services.exceptions import NotFoundError


class ActionService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.actions = ActionRepository(db)
        self.emails = EmailRepository(db)
        self.threads = ThreadRepository(db)
        self.audit = AuditService(db)

    def approve_reply(self, email_id: int) -> dict[str, str]:
        email = self.emails.get_by_id(email_id)
        if email is None:
            raise NotFoundError("Email not found.")
        self.actions.create(
            email_id=email.id,
            action_type="APPROVE_REPLY",
            reasoning="Reply draft approved for human send workflow.",
            status=Status.CLOSED,
        )
        self.audit.log_event("reply.approved", f"Reply approved for email_id={email.id}", email_id=email.id)
        self.db.commit()
        return {"status": "approved"}

    def escalate_thread(self, thread_id: int) -> dict[str, str]:
        thread = self.threads.get_by_id(thread_id)
        if thread is None:
            raise NotFoundError("Thread not found.")
        thread.status = Status.ESCALATED
        thread.priority = Priority.CRITICAL
        for email in thread.emails:
            self.actions.create(
                email_id=email.id,
                action_type="ESCALATE_THREAD",
                reasoning="Thread escalated by reviewer.",
                status=Status.ESCALATED,
            )
        self.audit.log_event("thread.escalated", f"Thread escalated thread_id={thread.id}")
        self.db.commit()
        return {"status": "escalated"}
