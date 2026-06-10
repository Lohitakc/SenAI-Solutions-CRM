from sqlalchemy.orm import Session

from app.models.classification import Classification


class ClassificationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        email_id: int,
        category: str,
        sentiment: str | None,
        urgency: str | None,
        confidence: float,
    ) -> Classification:
        classification = Classification(
            email_id=email_id,
            category=category,
            sentiment=sentiment,
            urgency=urgency,
            confidence=confidence,
        )
        self.db.add(classification)
        self.db.flush()
        return classification
