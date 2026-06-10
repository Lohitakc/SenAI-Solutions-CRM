from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.thread import Thread


class Contact(Base):
    __tablename__ = "contacts"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    company: Mapped[str | None] = mapped_column(String(255), nullable=True)

    threads: Mapped[list["Thread"]] = relationship(
        "Thread",
        back_populates="contact",
        lazy="selectin",
    )
