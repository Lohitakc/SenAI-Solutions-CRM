import json

from sqlalchemy.orm import Session

from app.repositories.agent_repository import AgentRepository
from app.schemas.ai import AIEmailRequest, AgentAnalyzeResponse, AgentHistoryResponse
from app.services.ai_classification_service import AIClassificationService
from app.services.crm_context_service import CRMContextService
from app.services.exceptions import NotFoundError
from app.services.retrieval_service import RetrievalService


class AgentService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.classification_service = AIClassificationService(db)
        self.retrieval_service = RetrievalService(db)
        self.crm_context = CRMContextService()
        self.repository = AgentRepository(db)

    def analyze(self, request: AIEmailRequest) -> AgentAnalyzeResponse:
        request = self._with_thread_history(request)
        tool_trace: list[dict[str, str]] = []
        profile = self.get_contact_profile(str(request.sender), tool_trace)
        account_status = self.check_account_status(str(request.sender), tool_trace)
        retrieved_chunks = self.search_knowledge_base(request, tool_trace)
        classification = self.classification_service.classify(request, persist=False)
        execution_plan = self._plan_actions(classification.human_required, classification.category, request.body)
        reasoning = self._build_reasoning(request, classification, profile, account_status, tool_trace)
        status = "ESCALATION_RECOMMENDED" if classification.human_required else "RECOMMENDATION_READY"
        if request.dry_run:
            status = f"DRY_RUN_{status}"

        log = self.repository.create(
            email_id=request.email_id,
            reasoning=reasoning,
            retrieved_chunks=json.dumps([chunk.model_dump() for chunk in retrieved_chunks or classification.retrieved_chunks]),
            prompt_metadata=json.dumps(
                {
                    "provider": "configured_llm_provider",
                    "thread_history_count": len(request.thread_history),
                    "dry_run": request.dry_run,
                    "contact_profile": profile,
                    "account_status": account_status,
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

    def search_knowledge_base(self, request: AIEmailRequest, trace: list[dict[str, str]]) -> list:
        chunks = self.retrieval_service.search(f"{request.subject or ''}\n{request.body}", top_k=3, threshold=0.0)
        trace.append({"Thought": "Need grounded policy context.", "Action": "search_knowledge_base", "Observation": f"Retrieved {len(chunks)} chunks.", "Next Thought": "Use sources in classification and reply planning."})
        return chunks

    def get_thread_history(self, request: AIEmailRequest, trace: list[dict[str, str]]) -> list[str]:
        history = list(request.thread_history)
        trace.append({"Thought": "Need full conversation context.", "Action": "get_thread_history", "Observation": f"Found {len(history)} prior messages.", "Next Thought": "Check CRM profile and account status."})
        return history

    def get_contact_profile(self, sender: str, trace: list[dict[str, str]]) -> dict:
        profile = self.crm_context.get_contact_profile(sender)
        trace.append({"Thought": "Need customer risk context.", "Action": "get_contact_profile", "Observation": f"VIP={profile.get('vip')} churn_risk={profile.get('churn_risk')}.", "Next Thought": "Check account status."})
        return profile

    def check_account_status(self, sender: str, trace: list[dict[str, str]]) -> dict:
        status = self.crm_context.check_account_status(sender)
        trace.append({"Thought": "Need billing and entitlement context.", "Action": "check_account_status", "Observation": f"billing_state={status.get('billing_state')} plan={status.get('plan')}.", "Next Thought": "Draft safe recommendation."})
        return status

    def draft_reply(self, classification, trace: list[dict[str, str]]) -> str:
        trace.append({"Thought": "Need human-safe response draft.", "Action": "draft_reply", "Observation": "Draft generated as recommendation only.", "Next Thought": "Determine escalation."})
        return classification.reply_draft

    def escalate_to_human(self, reason: str, trace: list[dict[str, str]]) -> str:
        trace.append({"Thought": "Risk requires human ownership.", "Action": "escalate_to_human", "Observation": reason, "Next Thought": "Create internal follow-up if needed."})
        return "Escalate to human owner."

    def create_internal_ticket(self, reason: str, trace: list[dict[str, str]]) -> str:
        trace.append({"Thought": "Internal team needs a trackable task.", "Action": "create_internal_ticket", "Observation": reason, "Next Thought": "Review legal/security flags."})
        return "Create internal ticket."

    def flag_for_legal(self, reason: str, trace: list[dict[str, str]]) -> str:
        trace.append({"Thought": "Legal/compliance exposure detected.", "Action": "flag_for_legal", "Observation": reason, "Next Thought": "Do not auto-reply."})
        return "Flag for legal review."

    def _plan_actions(self, human_required: bool, category: str, body: str) -> list[str]:
        actions = [
            "Review retrieved policy context.",
            "Send or edit the drafted customer reply.",
            "Record the final decision in the CRM timeline.",
        ]
        if human_required:
            actions.insert(1, "Escalate to a human owner before customer commitment.")
        if category in {"REFUND", "BILLING"}:
            actions.append("Route billing-related context to customer success.")
        if category in {"LEGAL", "COMPLIANCE", "SECURITY"} or any(
            keyword in body.lower() for keyword in ("ransomware", "gdpr", "lawsuit", "legal")
        ):
            actions.insert(0, "Do not auto-reply; require human approval.")
            actions.append("Flag legal/security/compliance owner before external response.")
        return actions

    def _build_reasoning(self, request: AIEmailRequest, classification, profile: dict, account_status: dict, trace: list[dict[str, str]]) -> str:
        self.draft_reply(classification, trace)
        if classification.human_required:
            self.escalate_to_human(f"{classification.category} requires review.", trace)
        if classification.category in {"LEGAL", "COMPLIANCE", "SECURITY"}:
            self.flag_for_legal(f"{classification.category} risk detected.", trace)
        limited_trace = trace[:6]
        return json.dumps(
            {
                "summary": f"Email from {request.sender} classified as {classification.category}.",
                "human_required": classification.human_required,
                "retrieved_chunk_count": len(classification.retrieved_chunks),
                "customer": {
                    "vip": profile.get("vip"),
                    "churn_risk": profile.get("churn_risk"),
                    "health_score": profile.get("customer_health_score"),
                },
                "account": {
                    "billing_state": account_status.get("billing_state"),
                    "plan": account_status.get("plan"),
                    "seat_count": account_status.get("seat_count"),
                },
                "trace": limited_trace,
            }
        )

    def _with_thread_history(self, request: AIEmailRequest) -> AIEmailRequest:
        if request.thread_history or request.email_id is None:
            return request
        from app.repositories.email_repository import EmailRepository

        email = EmailRepository(self.db).get_by_id(request.email_id)
        if email is None:
            return request
        history = [
            existing.body
            for existing in sorted(email.thread.emails, key=lambda item: item.received_at)
            if existing.id != request.email_id
        ]
        return request.model_copy(update={"thread_history": history})
