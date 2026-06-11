import logging
from pathlib import Path

from sqlalchemy.orm import Session

from app.repositories.knowledge_repository import KnowledgeRepository
from app.services.chroma_service import ChromaService
from app.services.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge_base"


class KnowledgeIngestionService:
    def __init__(
        self,
        db: Session,
        embedding_service: EmbeddingService | None = None,
        chroma_service: ChromaService | None = None,
    ) -> None:
        self.db = db
        self.repository = KnowledgeRepository(db)
        self.embedding_service = embedding_service or EmbeddingService()
        self.chroma_service = chroma_service or ChromaService()

    def ingest_directory(self, directory: Path = KNOWLEDGE_DIR) -> int:
        markdown_files = sorted(directory.glob("*.md"))
        ingested_count = 0
        for markdown_file in markdown_files:
            ingested_count += self.ingest_file(markdown_file)
        self.db.commit()
        logger.info("Knowledge ingestion completed with %s chunks.", ingested_count)
        return ingested_count

    def ingest_file(self, path: Path) -> int:
        content = path.read_text(encoding="utf-8")
        chunks = self._chunk_text(content)
        if not chunks:
            return 0

        ids = [f"{path.stem}-{index}" for index, _ in enumerate(chunks)]
        embeddings = self.embedding_service.embed(chunks)
        metadatas = [
            {
                "title": self._title_from_content(content, path.stem),
                "source_file": path.name,
                "chunk_index": index,
            }
            for index, _ in enumerate(chunks)
        ]
        self.chroma_service.upsert(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        stored = 0
        for chunk_id, chunk, metadata in zip(ids, chunks, metadatas, strict=True):
            if self.repository.get_by_embedding_reference(chunk_id) is None:
                self.repository.create(
                    title=str(metadata["title"]),
                    content=chunk,
                    embedding_reference=chunk_id,
                    source_file=str(metadata["source_file"]),
                    chunk_index=int(metadata["chunk_index"]),
                )
                stored += 1
        return stored

    def _chunk_text(self, content: str, max_words: int = 120, overlap: int = 20) -> list[str]:
        words = content.split()
        if not words:
            return []
        chunks: list[str] = []
        start = 0
        while start < len(words):
            end = min(start + max_words, len(words))
            chunks.append(" ".join(words[start:end]))
            if end == len(words):
                break
            start = max(end - overlap, start + 1)
        return chunks

    def _title_from_content(self, content: str, fallback: str) -> str:
        first_line = next((line.strip() for line in content.splitlines() if line.strip()), fallback)
        return first_line.lstrip("# ").strip() or fallback
