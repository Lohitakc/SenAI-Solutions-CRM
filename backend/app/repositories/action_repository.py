from sqlalchemy.orm import Session

from app.models.action import Action
from app.models.enums import Status


class ActionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, email_id: int, action_type: str, reasoning: str | None, status: Status) -> Action:
        action = Action(
            email_id=email_id,
            action_type=action_type,
            reasoning=reasoning,
            status=status,
        )
        self.db.add(action)
        self.db.flush()
        return action
