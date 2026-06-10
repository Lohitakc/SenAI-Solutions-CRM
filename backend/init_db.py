import logging

from app.db.init_db import init_db

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    init_db()
    logger.info("Database schema initialized successfully.")
