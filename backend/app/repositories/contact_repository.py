from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.contact import Contact
from app.models.email import Email
from app.models.thread import Thread


class ContactRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, contact_id: int) -> Contact | None:
        statement = (
            select(Contact)
            .options(selectinload(Contact.threads).selectinload(Thread.emails).selectinload(Email.classification))
            .where(Contact.id == contact_id)
        )
        return self.db.execute(statement).scalar_one_or_none()

    def list(self) -> list[Contact]:
        statement = (
            select(Contact)
            .options(selectinload(Contact.threads).selectinload(Thread.emails).selectinload(Email.classification))
            .order_by(Contact.created_at.desc())
        )
        return list(self.db.execute(statement).scalars().all())

    def get_by_email(self, email: str) -> Contact | None:
        statement = select(Contact).where(Contact.email == email)
        return self.db.execute(statement).scalar_one_or_none()

    def create(self, email: str, name: str | None, company: str | None) -> Contact:
        contact = Contact(email=email, name=name, company=company)
        self.db.add(contact)
        self.db.flush()
        return contact
