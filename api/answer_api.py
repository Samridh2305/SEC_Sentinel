from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_db
from retrieval.vector_retriever import VectorRetriever
from schema.schema import AnswerRequest, AnswerResponse
from services.answer_service import AnswerService
from embeddings.embedder import Embedder
from generation.answer_generator import AnswerGenerator

router = APIRouter(
    tags=["Answer"]
)

embedder = Embedder()

answer_generator = AnswerGenerator()

@router.post("/answer")
def answer(
    request: AnswerRequest,
        session: Session = Depends(get_db)
) -> AnswerResponse:

    retriever = VectorRetriever(
        session=session,
        embedder=embedder,
    )

    answer_service = AnswerService(
        retriever=retriever,
        answer_generator=answer_generator,
    )
    result = answer_service.answer(
        ticker=request.ticker,
        form_type=request.form_type,
        filing_date=request.filing_date,
        query=request.query,
        section=request.section
    )

    return AnswerResponse(
        answer=result.text
    )