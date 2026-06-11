from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.agent_reasoning import AgentReasoning


class AgentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        email_id: int | None,
        reasoning: str,
        retrieved_chunks: str,
        prompt_metadata: str,
        classification: str,
        reply_draft: str,
        execution_plan: str,
        status: str,
    ) -> AgentReasoning:
        log = AgentReasoning(
            email_id=email_id,
            reasoning=reasoning,
            retrieved_chunks=retrieved_chunks,
            prompt_metadata=prompt_metadata,
            classification=classification,
            reply_draft=reply_draft,
            execution_plan=execution_plan,
            status=status,
        )
        self.db.add(log)
        self.db.flush()
        return log

    def get_by_id(self, reasoning_id: int) -> AgentReasoning | None:
        statement = select(AgentReasoning).where(AgentReasoning.id == reasoning_id)
        return self.db.execute(statement).scalar_one_or_none()
