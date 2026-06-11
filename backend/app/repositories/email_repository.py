from datetime import datetime

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session, selectinload

from app.models.classification import Classification
from app.models.email import Email
from app.models.thread import Thread


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

    def list(
        self,
        search: str | None = None,
        priority: str | None = None,
        status: str | None = None,
        limit: int = 25,
        offset: int = 0,
        sort: str = "received_at_desc",
    ) -> list[Email]:
        statement: Select[tuple[Email]] = (
            select(Email)
            .join(Thread)
            .outerjoin(Classification)
            .options(selectinload(Email.classification), selectinload(Email.thread))
        )
        if search:
            pattern = f"%{search.lower()}%"
            statement = statement.where(
                func.lower(Email.sender).like(pattern)
                | func.lower(Email.subject).like(pattern)
                | func.lower(Email.body).like(pattern)
            )
        if priority:
            statement = statement.where(Thread.priority == priority)
        if status:
            statement = statement.where(Thread.status == status)
        if sort == "received_at_asc":
            statement = statement.order_by(Email.received_at.asc())
        else:
            statement = statement.order_by(Email.received_at.desc())
        statement = statement.limit(limit).offset(offset)
        return list(self.db.execute(statement).scalars().all())

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
