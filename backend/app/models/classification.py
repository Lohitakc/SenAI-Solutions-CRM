from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.email import Email


class Classification(Base):
    __tablename__ = "classifications"

    email_id: Mapped[int] = mapped_column(ForeignKey("emails.id"), unique=True, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    sentiment: Mapped[str | None] = mapped_column(String(100), nullable=True)
    urgency: Mapped[str | None] = mapped_column(String(100), nullable=True)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    human_required: Mapped[bool] = mapped_column(default=False, nullable=False)
    summary: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    reply_draft: Mapped[str | None] = mapped_column(String(4000), nullable=True)

    email: Mapped["Email"] = relationship(
        "Email",
        back_populates="classification",
        lazy="joined",
    )
