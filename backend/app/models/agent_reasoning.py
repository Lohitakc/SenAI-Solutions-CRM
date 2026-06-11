from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AgentReasoning(Base):
    __tablename__ = "agent_reasoning_logs"

    email_id: Mapped[int | None] = mapped_column(ForeignKey("emails.id"), index=True, nullable=True)
    reasoning: Mapped[str] = mapped_column(Text, nullable=False)
    retrieved_chunks: Mapped[str] = mapped_column(Text, nullable=False)
    prompt_metadata: Mapped[str] = mapped_column(Text, nullable=False)
    classification: Mapped[str] = mapped_column(Text, nullable=False)
    reply_draft: Mapped[str] = mapped_column(Text, nullable=False)
    execution_plan: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(100), nullable=False)
