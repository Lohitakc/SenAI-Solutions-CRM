from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.email import Email


class EmailRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, email_id: int) -> Email | None:
        statement = (
            select(Email)
            .options(selectinload(Email.classification))
            .where(Email.id == email_id)
        )
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_message_identifier(self, message_identifier: str) -> Email | None:
        statement = select(Email).where(Email.message_identifier == message_identifier)
        return self.db.execute(statement).scalar_one_or_none()

    def create(
        self,
        thread_id: int,
        message_identifier: str,
        sender: str,
        subject: str | None,
        body: str,
        received_at: datetime,
    ) -> Email:
        email = Email(
            thread_id=thread_id,
            message_identifier=message_identifier,
            sender=sender,
            subject=subject,
            body=body,
            received_at=received_at,
        )
        self.db.add(email)
        self.db.flush()
        return email
