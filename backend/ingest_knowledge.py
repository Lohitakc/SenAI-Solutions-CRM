import logging

from app.db.session import SessionLocal
from app.services.knowledge_ingestion_service import KnowledgeIngestionService

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    with SessionLocal() as db:
        count = KnowledgeIngestionService(db).ingest_directory()
    logger.info("Knowledge ingestion completed. New chunks stored: %s", count)
