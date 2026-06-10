from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.action import Action
    from app.models.classification import Classification
    from app.models.thread import Thread


class Email(Base):
    __tablename__ = "emails"

    thread_id: Mapped[int] = mapped_column(ForeignKey("threads.id"), nullable=False)
    message_identifier: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    sender: Mapped[str] = mapped_column(String(255), nullable=False)
    subject: Mapped[str | None] = mapped_column(String(500), nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    thread: Mapped["Thread"] = relationship(
        "Thread",
        back_populates="emails",
        lazy="joined",
    )
    classification: Mapped["Classification | None"] = relationship(
        "Classification",
        back_populates="email",
        uselist=False,
        lazy="selectin",
    )
    actions: Mapped[list["Action"]] = relationship(
        "Action",
        back_populates="email",
        lazy="selectin",
    )
