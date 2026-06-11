from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.ai import (
    AIClassificationResponse,
    AIEmailRequest,
    AgentAnalyzeResponse,
    AgentHistoryResponse,
    RagSearchRequest,
    RagSearchResponse,
    ReplyResponse,
)
from app.services.agent_service import AgentService
from app.services.ai_classification_service import AIClassificationService
from app.services.retrieval_service import RetrievalService

router = APIRouter()


@router.post(
    "/ai/classify",
    response_model=AIClassificationResponse,
    status_code=status.HTTP_200_OK,
    summary="Classify an email with retrieved context",
)
def classify_email(payload: AIEmailRequest, db: Session = Depends(get_db)) -> AIClassificationResponse:
    return AIClassificationService(db).classify(payload, persist=True)


@router.post(
    "/ai/reply",
    response_model=ReplyResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate a policy-grounded reply draft",
)
def generate_reply(payload: AIEmailRequest, db: Session = Depends(get_db)) -> ReplyResponse:
    reply_draft, chunks = AIClassificationService(db).generate_reply(payload)
    return ReplyResponse(reply_draft=reply_draft, retrieved_chunks=chunks)


@router.post(
    "/rag/search",
    response_model=RagSearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Search local knowledge-base chunks",
)
def search_knowledge(payload: RagSearchRequest, db: Session = Depends(get_db)) -> RagSearchResponse:
    chunks = RetrievalService(db).search(
        query=payload.query,
        top_k=payload.top_k,
        threshold=payload.threshold,
    )
    return RagSearchResponse(query=payload.query, chunks=chunks)


@router.post(
    "/agent/analyze",
    response_model=AgentAnalyzeResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze an email and recommend an execution plan",
)
def analyze_email(payload: AIEmailRequest, db: Session = Depends(get_db)) -> AgentAnalyzeResponse:
    return AgentService(db).analyze(payload)


@router.get(
    "/agent/history/{reasoning_id}",
    response_model=AgentHistoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Get stored agent reasoning history",
)
def get_agent_history(reasoning_id: int, db: Session = Depends(get_db)) -> AgentHistoryResponse:
    return AgentService(db).get_history(reasoning_id)
