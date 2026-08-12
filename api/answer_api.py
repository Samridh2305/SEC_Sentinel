from fastapi import APIRouter

from db.database import SessionLocal
from retrieval.vector_retriever import VectorRetriever
from schema.schema import AnswerRequest, AnswerResponse
from services.answer_service import AnswerService
from embeddings.embedder import Embedder
from generation.answer_generator import AnswerGenerator


router = APIRouter(
    tags=["Answer"]
)


session = SessionLocal()

embedder = Embedder()

answer_generator = AnswerGenerator()

retriever = VectorRetriever(
    session=session,
    embedder=embedder
)

answer_service = AnswerService(
    retriever=retriever,
    answer_generator=answer_generator
)


@router.post("/answer")
def answer(
    request: AnswerRequest
) -> AnswerResponse:

    result = answer_service.answer(
        ticker=request.ticker,
        form_type=request.form_type,
        filing_date=request.filing_date,
        query=request.query
    )

    return AnswerResponse(
        answer=result.text
    )