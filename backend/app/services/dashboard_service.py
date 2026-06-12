import json
from collections import Counter

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.agent_reasoning import AgentReasoning
from app.models.audit_log import AuditLog
from app.models.classification import Classification
from app.models.email import Email
from app.models.enums import Priority, Status
from app.models.knowledge_chunk import KnowledgeChunk
from app.models.thread import Thread
from app.repositories.email_repository import EmailRepository
from app.repositories.thread_repository import ThreadRepository
from app.schemas.dashboard import DashboardSummaryResponse, InboxEmailResponse, MetricPoint, ThreadDetailResponse


class DashboardService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.emails = EmailRepository(db)
        self.threads = ThreadRepository(db)

    def list_inbox(
        self,
        search: str | None,
        priority: str | None,
        status: str | None,
        limit: int,
        offset: int,
        sort: str,
    ) -> list[InboxEmailResponse]:
        emails = self.emails.list(search=search, priority=priority, status=status, limit=limit, offset=offset, sort=sort)
        return [
            InboxEmailResponse(
                id=email.id,
                thread_id=email.thread_id,
                sender=email.sender,
                subject=email.subject,
                received_at=email.received_at,
                priority=email.thread.priority,
                status=email.thread.status,
                category=email.classification.category if email.classification else None,
            )
            for email in emails
        ]

    def get_thread_detail(self, thread_id: int) -> ThreadDetailResponse:
        thread = self.threads.get_by_id(thread_id)
        if thread is None:
            from app.services.exceptions import NotFoundError

            raise NotFoundError("Thread not found.")
        return ThreadDetailResponse(
            id=thread.id,
            thread_identifier=thread.thread_identifier,
            contact_id=thread.contact_id,
            status=thread.status,
            priority=thread.priority,
            executive_summary=self._executive_thread_summary(thread) if len(thread.emails) >= 5 else None,
            policy_citations=self._thread_policy_citations(thread),
            emails=[
                {
                    "id": email.id,
                    "sender": email.sender,
                    "subject": email.subject,
                    "body": email.body,
                    "received_at": email.received_at.isoformat(),
                    "classification": {
                        "category": email.classification.category,
                        "sentiment": email.classification.sentiment,
                        "urgency": email.classification.urgency,
                        "confidence": email.classification.confidence,
                        "summary": email.classification.summary,
                        "reply_draft": email.classification.reply_draft,
                        "human_required": email.classification.human_required,
                    }
                    if email.classification
                    else None,
                }
                for email in thread.emails
            ],
        )

    def summary(self) -> DashboardSummaryResponse:
        total_emails = self.db.scalar(select(func.count()).select_from(Email)) or 0
        open_threads = self.db.scalar(select(func.count()).select_from(Thread).where(Thread.status == Status.OPEN)) or 0
        escalations = self.db.scalar(select(func.count()).select_from(Thread).where(Thread.priority == Priority.CRITICAL)) or 0
        human_required = self.db.scalar(select(func.count()).select_from(Classification).where(Classification.human_required.is_(True))) or 0
        average_confidence = self.db.scalar(select(func.avg(Classification.confidence))) or 0
        recent_logs = self.db.execute(select(AuditLog).order_by(AuditLog.created_at.desc()).limit(8)).scalars().all()
        return DashboardSummaryResponse(
            total_emails=total_emails,
            open_threads=open_threads,
            escalations=escalations,
            average_response_time="Pending",
            sentiment_distribution=self._count_distribution(Classification.sentiment, "Unspecified"),
            category_distribution=self._count_distribution(Classification.category, "GENERAL"),
            priority_distribution=self._count_distribution(Thread.priority, "MEDIUM"),
            daily_volume=self._daily_volume(),
            human_intervention_rate=round((human_required / total_emails) * 100, 2) if total_emails else 0.0,
            escalation_rate=round((escalations / total_emails) * 100, 2) if total_emails else 0.0,
            agent_confidence=round(float(average_confidence), 2),
            vip_customers=sum(1 for account in self._at_risk_accounts() if account.get("vip")),
            pending_approvals=self._pending_approvals(),
            knowledge_retrieval_count=self.db.scalar(select(func.count()).select_from(KnowledgeChunk)) or 0,
            most_retrieved_policy=self._most_retrieved_policy(),
            average_churn_score=self._average_churn_score(),
            top_complaint_categories=self._top_complaint_categories(),
            at_risk_accounts=self._at_risk_accounts(),
            critical_queue=self._critical_queue(),
            recent_activity=[
                {"id": log.id, "event": log.event, "details": log.details, "created_at": log.created_at.isoformat()}
                for log in recent_logs
            ],
        )

    def _count_distribution(self, column, fallback: str) -> list[MetricPoint]:
        rows = self.db.execute(select(column, func.count()).group_by(column)).all()
        return [MetricPoint(name=str(name or fallback), value=count) for name, count in rows]

    def _daily_volume(self) -> list[MetricPoint]:
        rows = self.db.execute(
            select(func.to_char(Email.received_at, "YYYY-MM-DD"), func.count())
            .group_by(func.to_char(Email.received_at, "YYYY-MM-DD"))
            .order_by(func.to_char(Email.received_at, "YYYY-MM-DD"))
        ).all()
        return [MetricPoint(name=day, value=count) for day, count in rows]

    def _top_complaint_categories(self) -> list[MetricPoint]:
        rows = self.db.execute(
            select(Classification.category, func.count())
            .where(Classification.sentiment == "NEGATIVE")
            .group_by(Classification.category)
            .order_by(func.count().desc())
            .limit(5)
        ).all()
        return [MetricPoint(name=str(category or "GENERAL"), value=count) for category, count in rows]

    def _critical_queue(self) -> list[dict]:
        rows = self.db.execute(
            select(Email)
            .join(Thread)
            .outerjoin(Classification)
            .where((Thread.priority == Priority.CRITICAL) | (Classification.human_required.is_(True)))
            .order_by(Email.received_at.desc())
            .limit(8)
        ).scalars().all()
        return [
            {
                "id": email.id,
                "thread_id": email.thread_id,
                "sender": email.sender,
                "subject": email.subject,
                "priority": email.thread.priority.value,
                "category": email.classification.category if email.classification else None,
            }
            for email in rows
        ]

    def _at_risk_accounts(self) -> list[dict]:
        rows = self.db.execute(
            select(Email.sender, func.count())
            .join(Thread)
            .where(Thread.priority.in_([Priority.HIGH, Priority.CRITICAL]))
            .group_by(Email.sender)
            .order_by(func.count().desc())
            .limit(5)
        ).all()
        return [
            {
                "sender": sender,
                "risk_events": count,
                "domain": sender.split("@")[-1] if "@" in sender else sender,
                "vip": sender.endswith("@enterprise.net"),
                "churn_score": min(100, 35 + (count * 12) + (20 if sender.endswith("@enterprise.net") else 0)),
            }
            for sender, count in rows
        ]

    def _pending_approvals(self) -> int:
        return self.db.scalar(
            select(func.count())
            .select_from(Classification)
            .where(Classification.human_required.is_(True))
        ) or 0

    def _most_retrieved_policy(self) -> str | None:
        rows = self.db.execute(select(AgentReasoning.retrieved_chunks).limit(200)).scalars().all()
        counter: Counter[str] = Counter()
        for row in rows:
            try:
                for chunk in json.loads(row):
                    source = chunk.get("source_file")
                    if source:
                        counter[source] += 1
            except (TypeError, ValueError, AttributeError):
                continue
        return counter.most_common(1)[0][0] if counter else None

    def _executive_thread_summary(self, thread: Thread) -> str:
        emails = sorted(thread.emails, key=lambda email: email.received_at)
        latest = emails[-1]
        categories = [
            email.classification.category
            for email in emails
            if email.classification is not None
        ]
        category_text = ", ".join(dict.fromkeys(categories[-4:])) or "general support"
        return (
            f"This thread contains {len(emails)} customer messages and is currently {thread.status.value.lower()} with {thread.priority.value.lower()} priority. "
            f"The conversation centers on {category_text}, with the latest message titled \"{latest.subject or 'No subject'}\". "
            "Recommended next step is to review the AI classification, confirm policy citations, and route any high-risk decision through human approval."
        )

    def _thread_policy_citations(self, thread: Thread) -> list[dict]:
        citations: dict[str, dict] = {}
        category_sources = {
            "REFUND": "refund_policy.md",
            "BILLING": "pricing_policy.md",
            "PRICING": "pricing_policy.md",
            "SLA": "sla_policy.md",
            "COMPLIANCE": "compliance_faq.md",
            "LEGAL": "escalation_matrix.md",
            "SECURITY": "escalation_matrix.md",
        }
        for email in thread.emails:
            category = email.classification.category if email.classification else None
            source = category_sources.get(str(category or "").upper())
            if source:
                citations[source] = {"source_file": source, "reason": f"Relevant to {category} classification"}
        return list(citations.values())

    def _average_churn_score(self) -> int:
        accounts = self._at_risk_accounts()
        if not accounts:
            return 0
        return round(sum(account["churn_score"] for account in accounts) / len(accounts))
