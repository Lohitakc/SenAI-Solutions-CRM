from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.knowledge_chunk import KnowledgeChunk


class KnowledgeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_embedding_reference(self, embedding_reference: str) -> KnowledgeChunk | None:
        statement = select(KnowledgeChunk).where(
            KnowledgeChunk.embedding_reference == embedding_reference
        )
        return self.db.execute(statement).scalar_one_or_none()

    def create(
        self,
        title: str,
        content: str,
        embedding_reference: str,
        source_file: str,
        chunk_index: int,
    ) -> KnowledgeChunk:
        chunk = KnowledgeChunk(
            title=title,
            content=content,
            embedding_reference=embedding_reference,
            source_file=source_file,
            chunk_index=chunk_index,
        )
        self.db.add(chunk)
        self.db.flush()
        return chunk
