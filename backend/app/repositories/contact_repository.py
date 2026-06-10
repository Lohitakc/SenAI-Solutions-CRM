from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.contact import Contact


class ContactRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, contact_id: int) -> Contact | None:
        return self.db.get(Contact, contact_id)

    def get_by_email(self, email: str) -> Contact | None:
        statement = select(Contact).where(Contact.email == email)
        return self.db.execute(statement).scalar_one_or_none()

    def create(self, email: str, name: str | None, company: str | None) -> Contact:
        contact = Contact(email=email, name=name, company=company)
        self.db.add(contact)
        self.db.flush()
        return contact
