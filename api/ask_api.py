from fastapi import (
    APIRouter,
    Depends
)
from sqlalchemy.orm import Session
from db.database import get_db
from db.repositories.filing_chunk_repository import FilingChunkRepository

from embeddings.embedder import Embedder

from retrieval.vector_retriever import VectorRetriever

from generation.answer_generator import AnswerGenerator
from generation.comparison_generator import ComparisonGenerator

from services.answer_service import AnswerService
from services.comparison_service import ComparisonService

from agents.graph import build_graph

from schema.schema import (
    AnswerRequest,
    AnswerResponse
)

router = APIRouter(
    tags=["AI"]
)

# Embedding

embedder = Embedder()

answer_generator = AnswerGenerator()

comparison_generator = ComparisonGenerator()

@router.post(
    "/ask",
    response_model=AnswerResponse
)
def ask(
    request: AnswerRequest,
    session: Session= Depends(get_db)
):
    retriever = VectorRetriever(
        session=session,
        embedder=embedder
    )

    # Answer service

    answer_service = AnswerService(
        retriever=retriever,
        answer_generator=answer_generator
    )

    repository = FilingChunkRepository(
        session=session
    )

    # Comparison service

    comparison_service = ComparisonService(
        repository=repository,
        comparison_generator=comparison_generator
    )

    graph = build_graph(
        answer_service=answer_service,
        comparison_service=comparison_service
    )
    result = graph.invoke(
        {
            "ticker": request.ticker,
            "form_type": request.form_type,
            "filing_date": request.filing_date,
            "comparison_filing_date": request.comparison_filing_date,
            "section": request.section,
            "query": request.query,

            "route": None,
            "answer": None
        }
    )

    return AnswerResponse(
        answer=result["answer"]
    )
