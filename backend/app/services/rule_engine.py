from dataclasses import dataclass

from app.models.enums import Priority


@dataclass(frozen=True)
class Rule:
    keyword: str
    category: str | None = None
    priority: Priority | None = None
    sentiment: str | None = None
    urgency: str | None = None


@dataclass(frozen=True)
class ClassificationResult:
    category: str
    priority: Priority
    sentiment: str | None
    urgency: str | None
    confidence: float


class RuleEngine:
    def __init__(
        self,
        content_rules: tuple[Rule, ...] | None = None,
        internal_domains: tuple[str, ...] = ("senai.com",),
    ) -> None:
        self.content_rules = content_rules or (
            Rule(keyword="ransomware", category="SECURITY", priority=Priority.CRITICAL, urgency="CRITICAL"),
            Rule(keyword="data breach", category="SECURITY", priority=Priority.CRITICAL, urgency="CRITICAL"),
            Rule(keyword="suspicious login", category="SECURITY", priority=Priority.CRITICAL, urgency="CRITICAL"),
            Rule(keyword="gdpr", category="COMPLIANCE", priority=Priority.CRITICAL, urgency="CRITICAL"),
            Rule(keyword="article 20", category="COMPLIANCE", priority=Priority.CRITICAL, urgency="CRITICAL"),
            Rule(keyword="cease and desist", category="LEGAL", priority=Priority.CRITICAL, urgency="CRITICAL"),
            Rule(keyword="lawsuit", category="LEGAL", priority=Priority.CRITICAL, urgency="CRITICAL"),
            Rule(keyword="p0", category="SLA", priority=Priority.CRITICAL, urgency="CRITICAL"),
            Rule(keyword="legal", priority=Priority.CRITICAL, urgency="CRITICAL"),
            Rule(keyword="urgent", priority=Priority.HIGH, urgency="HIGH"),
            Rule(keyword="sla", category="SLA", priority=Priority.HIGH, urgency="HIGH"),
            Rule(keyword="outage", category="SLA", priority=Priority.HIGH, urgency="HIGH"),
            Rule(keyword="bug", category="BUG_REPORT", priority=Priority.HIGH, sentiment="NEGATIVE"),
            Rule(keyword="incorrect", category="COMPLAINT", sentiment="NEGATIVE"),
            Rule(keyword="refund", category="REFUND"),
            Rule(keyword="invoice", category="BILLING"),
            Rule(keyword="pricing", category="PRICING"),
            Rule(keyword="discount", category="PRICING"),
            Rule(keyword="complaint", category="COMPLAINT", sentiment="NEGATIVE"),
            Rule(keyword="cancel", category="CANCELLATION"),
            Rule(keyword="spam", category="SPAM", priority=Priority.LOW),
            Rule(keyword="seo", category="SPAM", priority=Priority.LOW),
            Rule(keyword="thank", category="POSITIVE", sentiment="POSITIVE"),
        )
        self.internal_domains = tuple(domain.lower() for domain in internal_domains)

    def classify(self, sender: str, subject: str | None, body: str) -> ClassificationResult:
        sender_normalized = sender.lower().strip()
        text = f"{subject or ''} {body}".lower()
        category = "GENERAL"
        priority = Priority.MEDIUM
        sentiment: str | None = None
        urgency: str | None = None

        if sender_normalized.startswith("noreply@") or sender_normalized.startswith("no-reply@"):
            category = "SYSTEM"
        elif self._is_internal_sender(sender_normalized):
            category = "INTERNAL"

        for rule in self.content_rules:
            if rule.keyword in text:
                if rule.category is not None and category == "GENERAL":
                    category = rule.category
                if rule.priority is not None:
                    priority = self._max_priority(priority, rule.priority)
                if rule.sentiment is not None:
                    sentiment = rule.sentiment
                if rule.urgency is not None:
                    urgency = rule.urgency

        return ClassificationResult(
            category=category,
            priority=priority,
            sentiment=sentiment,
            urgency=urgency,
            confidence=1.0,
        )

    def _is_internal_sender(self, sender: str) -> bool:
        return any(sender.endswith(f"@{domain}") for domain in self.internal_domains)

    def _max_priority(self, current: Priority, candidate: Priority) -> Priority:
        order = {
            Priority.LOW: 1,
            Priority.MEDIUM: 2,
            Priority.HIGH: 3,
            Priority.CRITICAL: 4,
        }
        return candidate if order[candidate] > order[current] else current
