from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import Priority, Status

if TYPE_CHECKING:
    from app.models.contact import Contact
    from app.models.email import Email


class Thread(Base):
    __tablename__ = "threads"

    thread_identifier: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    contact_id: Mapped[int] = mapped_column(ForeignKey("contacts.id"), index=True, nullable=False)
    status: Mapped[Status] = mapped_column(
        Enum(Status, name="thread_status"),
        default=Status.OPEN,
        index=True,
        nullable=False,
    )
    priority: Mapped[Priority] = mapped_column(
        Enum(Priority, name="thread_priority"),
        default=Priority.MEDIUM,
        index=True,
        nullable=False,
    )

    contact: Mapped["Contact"] = relationship(
        "Contact",
        back_populates="threads",
        lazy="joined",
    )
    emails: Mapped[list["Email"]] = relationship(
        "Email",
        back_populates="thread",
        lazy="selectin",
    )
