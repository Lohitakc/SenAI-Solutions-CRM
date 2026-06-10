from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.email import Email


class AuditLog(Base):
    __tablename__ = "audit_logs"

    event: Mapped[str] = mapped_column(Text, nullable=False)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    email_id: Mapped[int | None] = mapped_column(ForeignKey("emails.id"), index=True, nullable=True)

    email: Mapped["Email | None"] = relationship(
        "Email",
        lazy="joined",
    )
