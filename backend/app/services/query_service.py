from sqlalchemy.orm import Session

from app.models.contact import Contact
from app.models.thread import Thread
from app.repositories.contact_repository import ContactRepository
from app.repositories.thread_repository import ThreadRepository
from app.services.crm_context_service import CRMContextService
from app.services.exceptions import NotFoundError


class QueryService:
    def __init__(self, db: Session) -> None:
        self.contacts = ContactRepository(db)
        self.threads = ThreadRepository(db)
        self.crm_context = CRMContextService()

    def get_contact(self, contact_id: int) -> Contact:
        contact = self.contacts.get_by_id(contact_id)
        if contact is None:
            raise NotFoundError("Contact not found.")
        return contact

    def list_customer_profiles(self) -> list[dict]:
        return [self._customer_profile(contact) for contact in self.contacts.list()]

    def get_customer_profile(self, contact_id: int) -> dict:
        contact = self.contacts.get_by_id(contact_id)
        if contact is None:
            raise NotFoundError("Contact not found.")
        return self._customer_profile(contact)

    def get_thread(self, thread_id: int) -> Thread:
        thread = self.threads.get_by_id(thread_id)
        if thread is None:
            raise NotFoundError("Thread not found.")
        return thread

    def _customer_profile(self, contact: Contact) -> dict:
        profile = self.crm_context.get_contact_profile(contact.email)
        account = self.crm_context.check_account_status(contact.email)
        emails = [email for thread in contact.threads for email in thread.emails]
        emails.sort(key=lambda email: email.received_at, reverse=True)
        analyses = [
            {
                "email_id": email.id,
                "category": email.classification.category,
                "urgency": email.classification.urgency,
                "confidence": email.classification.confidence,
                "human_required": email.classification.human_required,
            }
            for email in emails
            if email.classification is not None
        ][:5]
        return {
            "id": contact.id,
            "email": contact.email,
            "name": contact.name,
            "company": contact.company,
            "created_at": contact.created_at.isoformat(),
            "profile": profile,
            "account_status": account,
            "churn_prediction_score": self._churn_prediction_score(profile, account, analyses, emails),
            "churn_prediction_factors": self._churn_prediction_factors(profile, account, analyses, emails),
            "recent_conversations": [
                {
                    "id": email.id,
                    "thread_id": email.thread_id,
                    "subject": email.subject,
                    "received_at": email.received_at.isoformat(),
                    "category": email.classification.category if email.classification else None,
                }
                for email in emails[:5]
            ],
            "ai_analyses": analyses,
            "recommended_actions": self._recommended_actions(profile, account, analyses),
        }

    def _recommended_actions(self, profile: dict, account: dict, analyses: list[dict]) -> list[str]:
        actions: list[str] = []
        if profile.get("vip"):
            actions.append("Assign account manager follow-up within one business hour.")
        if profile.get("churn_risk") in {"high", "critical"}:
            actions.append("Create retention plan and review recent negative conversations.")
        if account.get("billing_state") == "at_risk" or account.get("overdue_invoices"):
            actions.append("Coordinate billing review before promising credits or renewals.")
        if any(item.get("human_required") for item in analyses):
            actions.append("Review AI escalations before sending customer response.")
        return actions or ["Monitor account health and continue standard support workflow."]

    def _churn_prediction_score(self, profile: dict, account: dict, analyses: list[dict], emails: list) -> int:
        score = 20
        if profile.get("churn_risk") == "critical":
            score += 35
        elif profile.get("churn_risk") == "high":
            score += 25
        elif profile.get("churn_risk") == "medium":
            score += 12
        score += max(0, 70 - int(profile.get("customer_health_score") or 70)) // 2
        score += min(20, sum(1 for item in analyses if item.get("human_required")) * 8)
        score += min(15, sum(1 for item in analyses if item.get("category") in {"COMPLAINT", "REFUND", "CANCELLATION", "SLA"}) * 5)
        if account.get("billing_state") == "at_risk" or account.get("overdue_invoices"):
            score += 10
        if len(emails) >= 3:
            score += 5
        return min(100, score)

    def _churn_prediction_factors(self, profile: dict, account: dict, analyses: list[dict], emails: list) -> list[str]:
        factors: list[str] = []
        factors.append(f"CRM churn risk is {profile.get('churn_risk', 'unknown')}.")
        factors.append(f"Customer health score is {profile.get('customer_health_score', 'unknown')}.")
        if any(item.get("human_required") for item in analyses):
            factors.append("Escalation history includes human-review items.")
        if any(item.get("category") in {"COMPLAINT", "REFUND", "CANCELLATION", "SLA"} for item in analyses):
            factors.append("Category history includes complaint, refund, cancellation, or SLA risk.")
        if account.get("billing_state") == "at_risk" or account.get("overdue_invoices"):
            factors.append("Account status shows billing risk.")
        if len(emails) >= 3:
            factors.append("Response history includes multiple messages in the relationship.")
        return factors
