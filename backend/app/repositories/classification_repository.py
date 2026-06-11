from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.classification import Classification


class ClassificationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_email_id(self, email_id: int) -> Classification | None:
        statement = select(Classification).where(Classification.email_id == email_id)
        return self.db.execute(statement).scalar_one_or_none()

    def create(
        self,
        email_id: int,
        category: str,
        sentiment: str | None,
        urgency: str | None,
        confidence: float,
        human_required: bool = False,
        summary: str | None = None,
        reply_draft: str | None = None,
    ) -> Classification:
        classification = Classification(
            email_id=email_id,
            category=category,
            sentiment=sentiment,
            urgency=urgency,
            confidence=confidence,
            human_required=human_required,
            summary=summary,
            reply_draft=reply_draft,
        )
        self.db.add(classification)
        self.db.flush()
        return classification

    def upsert(
        self,
        email_id: int,
        category: str,
        sentiment: str | None,
        urgency: str | None,
        confidence: float,
        human_required: bool,
        summary: str | None,
        reply_draft: str | None,
    ) -> Classification:
        classification = self.get_by_email_id(email_id)
        if classification is None:
            return self.create(
                email_id=email_id,
                category=category,
                sentiment=sentiment,
                urgency=urgency,
                confidence=confidence,
                human_required=human_required,
                summary=summary,
                reply_draft=reply_draft,
            )
        classification.category = category
        classification.sentiment = sentiment
        classification.urgency = urgency
        classification.confidence = confidence
        classification.human_required = human_required
        classification.summary = summary
        classification.reply_draft = reply_draft
        self.db.flush()
        return classification
