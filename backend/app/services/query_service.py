from sqlalchemy.orm import Session

from app.models.contact import Contact
from app.models.thread import Thread
from app.repositories.contact_repository import ContactRepository
from app.repositories.thread_repository import ThreadRepository
from app.services.exceptions import NotFoundError


class QueryService:
    def __init__(self, db: Session) -> None:
        self.contacts = ContactRepository(db)
        self.threads = ThreadRepository(db)

    def get_contact(self, contact_id: int) -> Contact:
        contact = self.contacts.get_by_id(contact_id)
        if contact is None:
            raise NotFoundError("Contact not found.")
        return contact

    def get_thread(self, thread_id: int) -> Thread:
        thread = self.threads.get_by_id(thread_id)
        if thread is None:
            raise NotFoundError("Thread not found.")
        return thread
