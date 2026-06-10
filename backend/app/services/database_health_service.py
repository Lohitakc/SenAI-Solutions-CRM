import logging

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class DatabaseHealthService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def check(self) -> dict[str, str]:
        try:
            self.db.execute(text("SELECT 1"))
            return {"status": "healthy"}
        except SQLAlchemyError:
            logger.exception("Database health check failed")
            return {"status": "unhealthy"}
