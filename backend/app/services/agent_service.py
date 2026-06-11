import json

from sqlalchemy.orm import Session

from app.repositories.agent_repository import AgentRepository
from app.schemas.ai import AIEmailRequest, AgentAnalyzeResponse, AgentHistoryResponse
from app.services.ai_classification_service import AIClassificationService
from app.services.exceptions import NotFoundError


class AgentService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.classification_service = AIClassificationService(db)
        self.repository = AgentRepository(db)

    def analyze(self, request: AIEmailRequest) -> AgentAnalyzeResponse:
        classification = self.classification_service.classify(request, persist=False)
        execution_plan = self._plan_actions(classification.human_required, classification.category)
        reasoning = self._build_reasoning(request, classification)
        status = "ESCALATION_RECOMMENDED" if classification.human_required else "RECOMMENDATION_READY"

        log = self.repository.create(
            email_id=request.email_id,
            reasoning=reasoning,
            retrieved_chunks=json.dumps([chunk.model_dump() for chunk in classification.retrieved_chunks]),
            prompt_metadata=json.dumps(
                {
                    "provider": "configured_llm_provider",
                    "thread_history_count": len(request.thread_history),
                }
            ),
            classification=classification.model_dump_json(),
            reply_draft=classification.reply_draft,
            execution_plan=json.dumps(execution_plan),
            status=status,
        )
        self.db.commit()
        self.db.refresh(log)

        return AgentAnalyzeResponse(
            reasoning_id=log.id,
            reasoning=reasoning,
            classification=classification,
            execution_plan=execution_plan,
            escalation_required=classification.human_required,
            status=status,
        )

    def get_history(self, reasoning_id: int) -> AgentHistoryResponse:
        log = self.repository.get_by_id(reasoning_id)
        if log is None:
            raise NotFoundError("Agent reasoning history not found.")
        return AgentHistoryResponse.model_validate(log)

    def _plan_actions(self, human_required: bool, category: str) -> list[str]:
        actions = [
            "Review retrieved policy context.",
            "Send or edit the drafted customer reply.",
            "Record the final decision in the CRM timeline.",
        ]
        if human_required:
            actions.insert(1, "Escalate to a human owner before customer commitment.")
        if category in {"REFUND", "BILLING"}:
            actions.append("Route billing-related context to customer success.")
        return actions

    def _build_reasoning(self, request: AIEmailRequest, classification) -> str:
        return (
            f"Email from {request.sender} was classified as {classification.category}. "
            f"Human review required: {classification.human_required}. "
            f"Retrieved {len(classification.retrieved_chunks)} knowledge chunks before drafting a reply."
        )
