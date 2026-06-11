from sqlalchemy.orm import Session

from app.schemas.ai import RetrievedChunkResponse
from app.services.chroma_service import ChromaService
from app.services.embedding_service import EmbeddingService


class RetrievalService:
    def __init__(
        self,
        db: Session,
        embedding_service: EmbeddingService | None = None,
        chroma_service: ChromaService | None = None,
    ) -> None:
        self.db = db
        self.embedding_service = embedding_service or EmbeddingService()
        self.chroma_service = chroma_service or ChromaService()

    def search(self, query: str, top_k: int = 3, threshold: float = 0.0) -> list[RetrievedChunkResponse]:
        query_embedding = self.embedding_service.embed([query])[0]
        result = self.chroma_service.query(query_embedding=query_embedding, top_k=top_k)
        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0]
        ids = result.get("ids", [[]])[0]

        chunks: list[RetrievedChunkResponse] = []
        for document, metadata, distance, chunk_id in zip(documents, metadatas, distances, ids, strict=False):
            score = max(0.0, 1.0 - float(distance))
            if score < threshold:
                continue
            chunks.append(
                RetrievedChunkResponse(
                    content=document,
                    title=metadata.get("title") if metadata else None,
                    source_file=metadata.get("source_file") if metadata else None,
                    score=score,
                    embedding_reference=chunk_id,
                )
            )
        return chunks
