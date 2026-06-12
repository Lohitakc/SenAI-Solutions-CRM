import json
from datetime import UTC, datetime

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

    def approve_reply(self, email_id: int, edited_draft: str | None = None) -> dict[str, str]:
        email = self.emails.get_by_id(email_id)
        if email is None:
            raise NotFoundError("Email not found.")
        original_draft = email.classification.reply_draft if email.classification else ""
        final_draft = edited_draft if edited_draft is not None else original_draft
        training_pair = {
            "original_ai_draft": original_draft,
            "edited_draft": final_draft,
            "approval_status": "approved",
            "approved_at": datetime.now(UTC).isoformat(),
            "delta": self._draft_delta(original_draft or "", final_draft or ""),
        }
        self.actions.create(
            email_id=email.id,
            action_type="APPROVE_REPLY",
            reasoning=json.dumps(training_pair),
            status=Status.CLOSED,
        )
        self.audit.log_event("reply.approved", f"Reply approved for email_id={email.id}", email_id=email.id)
        self.db.commit()
        return {"status": "approved"}

    def _draft_delta(self, original: str, edited: str) -> str:
        if original == edited:
            return "No edits made before approval."
        return f"Original length {len(original)} chars; edited length {len(edited)} chars."

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
