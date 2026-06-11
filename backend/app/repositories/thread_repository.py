from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.enums import Priority, Status
from app.models.thread import Thread
from app.models.email import Email


class ThreadRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, thread_id: int) -> Thread | None:
        statement = (
            select(Thread)
            .options(selectinload(Thread.emails).selectinload(Email.classification))
            .where(Thread.id == thread_id)
        )
        return self.db.execute(statement).scalar_one_or_none()

    def get_by_identifier(self, thread_identifier: str) -> Thread | None:
        statement = select(Thread).where(Thread.thread_identifier == thread_identifier)
        return self.db.execute(statement).scalar_one_or_none()

    def create(
        self,
        thread_identifier: str,
        contact_id: int,
        status: Status,
        priority: Priority,
    ) -> Thread:
        thread = Thread(
            thread_identifier=thread_identifier,
            contact_id=contact_id,
            status=status,
            priority=priority,
        )
        self.db.add(thread)
        self.db.flush()
        return thread

    def update_priority(self, thread: Thread, priority: Priority) -> Thread:
        thread.priority = priority
        self.db.flush()
        return thread
