from fastapi import APIRouter

from db.database import SessionLocal
from db.repositories.filing_chunk_repository import FilingChunkRepository

from generation.comparison_generator import ComparisonGenerator

from schema.schema import (
    ComparisonRequest,
    ComparisonResponse
)

from services.comparison_service import ComparisonService


router = APIRouter(
    tags=["Compare"]
)


session = SessionLocal()

repository = FilingChunkRepository(
    session=session
)

comparison_generator = ComparisonGenerator()

comparison_service = ComparisonService(
    repository=repository,
    comparison_generator=comparison_generator
)


@router.post("/comparison")
def comparison(
    request: ComparisonRequest
) -> ComparisonResponse:

    result = comparison_service.compare(
        ticker=request.ticker,
        form_type=request.form_type,
        filing_date=request.filing_date,
        section=request.section,
        query=request.query
    )

    return ComparisonResponse(
        comparison=result.text
    )