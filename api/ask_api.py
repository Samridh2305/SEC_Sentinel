from fastapi import APIRouter

from db.database import SessionLocal
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


# -------------------------
# Database
# -------------------------

session = SessionLocal()


# -------------------------
# Embedding / Retrieval
# -------------------------

embedder = Embedder()

retriever = VectorRetriever(
    session=session,
    embedder=embedder
)


# -------------------------
# Answer service
# -------------------------

answer_generator = AnswerGenerator()

answer_service = AnswerService(
    retriever=retriever,
    answer_generator=answer_generator
)


# -------------------------
# Comparison service
# -------------------------

comparison_generator = ComparisonGenerator()

repository = FilingChunkRepository(
    session=session
)

comparison_service = ComparisonService(
    repository=repository,
    comparison_generator=comparison_generator
)


# -------------------------
# LangGraph
# -------------------------

graph = build_graph(
    answer_service=answer_service,
    comparison_service=comparison_service
)


# -------------------------
# API
# -------------------------

@router.post(
    "/ask",
    response_model=AnswerResponse
)
def ask(
    request: AnswerRequest
):

    result = graph.invoke(
        {
            "ticker": request.ticker,
            "form_type": request.form_type,
            "filing_date": request.filing_date,
            "section": request.section,
            "query": request.query,

            "route": None,
            "answer": None
        }
    )

    return AnswerResponse(
        answer=result["answer"]
    )