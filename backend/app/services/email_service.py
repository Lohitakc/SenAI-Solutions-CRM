import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.email import Email
from app.models.enums import Priority, Status
from app.repositories.classification_repository import ClassificationRepository
from app.repositories.contact_repository import ContactRepository
from app.repositories.email_repository import EmailRepository
from app.repositories.thread_repository import ThreadRepository
from app.schemas.email import EmailCreate
from app.services.audit_service import AuditService
from app.services.exceptions import DuplicateEmailError, NotFoundError
from app.services.rule_engine import RuleEngine

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self, db: Session, rule_engine: RuleEngine | None = None) -> None:
        self.db = db
        self.contacts = ContactRepository(db)
        self.threads = ThreadRepository(db)
        self.emails = EmailRepository(db)
        self.classifications = ClassificationRepository(db)
        self.audit = AuditService(db)
        self.rule_engine = rule_engine or RuleEngine()

    def ingest_email(self, payload: EmailCreate) -> Email:
        email_id: int | None = None
        try:
            contact_email = payload.contact_email.lower().strip()
            sender = payload.sender.lower().strip()
            thread_identifier = payload.thread_identifier.strip()
            message_identifier = payload.message_identifier.strip()

            if self.emails.get_by_message_identifier(message_identifier):
                logger.warning("Duplicate email rejected: %s", message_identifier)
                self.audit.log_event(
                    event="email.duplicate_rejected",
                    details=f"Duplicate message_identifier={message_identifier}",
                )
                self.db.commit()
                raise DuplicateEmailError("Email with this message_identifier already exists.")

            classification_result = self.rule_engine.classify(
                sender=sender,
                subject=payload.subject,
                body=payload.body,
            )

            contact = self.contacts.get_by_email(contact_email)
            if contact is None:
                contact = self.contacts.create(
                    email=contact_email,
                    name=payload.contact_name,
                    company=payload.company,
                )

            thread = self.threads.get_by_identifier(thread_identifier)
            if thread is None:
                thread = self.threads.create(
                    thread_identifier=thread_identifier,
                    contact_id=contact.id,
                    status=Status.OPEN,
                    priority=classification_result.priority,
                )
            elif self._priority_rank(classification_result.priority) > self._priority_rank(thread.priority):
                self.threads.update_priority(thread=thread, priority=classification_result.priority)

            email = self.emails.create(
                thread_id=thread.id,
                message_identifier=message_identifier,
                sender=sender,
                subject=payload.subject,
                body=payload.body,
                received_at=payload.received_at,
            )
            email_id = email.id

            classification = self.classifications.create(
                email_id=email.id,
                category=classification_result.category,
                sentiment=classification_result.sentiment,
                urgency=classification_result.urgency,
                confidence=classification_result.confidence,
            )
            email.classification = classification

            self.audit.log_event(
                event="email.ingested",
                details=f"Email ingested with message_identifier={message_identifier}",
                email_id=email.id,
            )
            self.db.commit()
            self.db.refresh(email)
            logger.info("Email ingested successfully: %s", message_identifier)
            return email
        except DuplicateEmailError:
            raise
        except SQLAlchemyError as exc:
            self.db.rollback()
            logger.exception("Database error during email ingestion")
            self._log_error_safely("email.ingestion_failed", str(exc), email_id)
            raise
        except Exception as exc:
            self.db.rollback()
            logger.exception("Unexpected error during email ingestion")
            self._log_error_safely("email.ingestion_failed", str(exc), email_id)
            raise

    def get_email(self, email_id: int) -> Email:
        email = self.emails.get_by_id(email_id)
        if email is None:
            raise NotFoundError("Email not found.")
        return email

    def _log_error_safely(self, event: str, details: str, email_id: int | None) -> None:
        try:
            self.audit.log_event(event=event, details=details, email_id=email_id)
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            logger.exception("Failed to write audit error event")

    def _priority_rank(self, priority: Priority) -> int:
        return {
            Priority.LOW: 1,
            Priority.MEDIUM: 2,
            Priority.HIGH: 3,
            Priority.CRITICAL: 4,
        }[priority]
