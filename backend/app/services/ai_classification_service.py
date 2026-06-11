from sqlalchemy.orm import Session

from app.repositories.classification_repository import ClassificationRepository
from app.schemas.ai import AIClassificationResponse, AIEmailRequest, RetrievedChunkResponse
from app.services.llm_factory import get_llm_provider
from app.services.llm_provider import LLMProvider
from app.services.retrieval_service import RetrievalService
from app.services.rule_engine import RuleEngine


class AIClassificationService:
    def __init__(
        self,
        db: Session,
        retrieval_service: RetrievalService | None = None,
        llm_provider: LLMProvider | None = None,
    ) -> None:
        self.db = db
        self.retrieval_service = retrieval_service or RetrievalService(db)
        self.llm_provider = llm_provider or get_llm_provider()
        self.rule_engine = RuleEngine()
        self.classifications = ClassificationRepository(db)

    def classify(self, request: AIEmailRequest, persist: bool = True) -> AIClassificationResponse:
        query = f"{request.subject or ''}\n{request.body}"
        chunks = self.retrieval_service.search(query=query, top_k=3, threshold=0.0)
        rule_result = self.rule_engine.classify(
            sender=str(request.sender),
            subject=request.subject,
            body=request.body,
        )
        summary = self._summarize(request, chunks)
        reply_draft = self._draft_reply(request, chunks)
        human_required = self._requires_human(rule_result.priority.value, request.body)

        response = AIClassificationResponse(
            category=rule_result.category,
            sentiment=rule_result.sentiment,
            urgency=rule_result.urgency,
            confidence=rule_result.confidence,
            human_required=human_required,
            summary=summary,
            reply_draft=reply_draft,
            retrieved_chunks=chunks,
        )

        if persist and request.email_id is not None:
            self.classifications.upsert(
                email_id=request.email_id,
                category=response.category,
                sentiment=response.sentiment,
                urgency=response.urgency,
                confidence=response.confidence,
                human_required=response.human_required,
                summary=response.summary,
                reply_draft=response.reply_draft,
            )
            self.db.commit()

        return response

    def generate_reply(self, request: AIEmailRequest) -> tuple[str, list[RetrievedChunkResponse]]:
        chunks = self.retrieval_service.search(
            query=f"{request.subject or ''}\n{request.body}",
            top_k=3,
            threshold=0.0,
        )
        return self._draft_reply(request, chunks), chunks

    def _summarize(self, request: AIEmailRequest, chunks: list[RetrievedChunkResponse]) -> str:
        context = self._context_text(chunks)
        prompt = (
            "Summarize this CRM email in one concise sentence using only the provided context and thread history.\n"
            f"Subject: {request.subject}\nBody: {request.body}\nContext: {context}"
            f"\nThread history: {self._thread_history_text(request.thread_history)}"
        )
        return self.llm_provider.generate(prompt)

    def _draft_reply(self, request: AIEmailRequest, chunks: list[RetrievedChunkResponse]) -> str:
        context = self._context_text(chunks)
        prompt = (
            "Draft a concise, professional customer support reply. Use only the provided CRM policy context. "
            "Do not invent policy details. Reference the relevant policy source by name when useful. "
            "If this is legal, ransomware, GDPR, security, or critical SLA risk, do not auto-reply; draft an internal escalation note.\n"
            f"Subject: {request.subject}\nBody: {request.body}\nContext: {context}"
            f"\nThread history: {self._thread_history_text(request.thread_history)}"
        )
        return self.llm_provider.generate(prompt)

    def _context_text(self, chunks: list[RetrievedChunkResponse]) -> str:
        if not chunks:
            return "No relevant context retrieved."
        return "\n\n".join(
            f"Source: {chunk.source_file or 'unknown'} | Score: {chunk.score:.3f}\n{chunk.content}"
            for chunk in chunks
        )

    def _requires_human(self, priority: str, body: str) -> bool:
        body_lower = body.lower()
        return priority == "CRITICAL" or any(
            keyword in body_lower
            for keyword in ("legal", "compliance", "breach", "lawsuit", "security", "ransomware", "gdpr")
        )

    def _thread_history_text(self, thread_history: list[str]) -> str:
        if not thread_history:
            return "No previous thread history provided."
        return "\n".join(f"{index + 1}. {item[:1000]}" for index, item in enumerate(thread_history[-10:]))
