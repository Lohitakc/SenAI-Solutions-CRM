from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import Status

if TYPE_CHECKING:
    from app.models.email import Email


class Action(Base):
    __tablename__ = "actions"

    email_id: Mapped[int] = mapped_column(ForeignKey("emails.id"), nullable=False)
    action_type: Mapped[str] = mapped_column(String(100), nullable=False)
    reasoning: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[Status] = mapped_column(
        Enum(Status, name="action_status"),
        default=Status.PENDING,
        index=True,
        nullable=False,
    )

    email: Mapped["Email"] = relationship(
        "Email",
        back_populates="actions",
        lazy="joined",
    )
