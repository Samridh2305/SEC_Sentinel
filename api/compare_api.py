from fastapi import (
    APIRouter,
    Depends)
from sqlalchemy.orm import Session

from db.database import get_db
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

comparison_generator = ComparisonGenerator()

@router.post("/comparison")
def comparison(
    request: ComparisonRequest,
    session: Session = Depends(get_db),
) -> ComparisonResponse:

    repository = FilingChunkRepository(
        session=session
    )

    comparison_service = ComparisonService(
        repository=repository,
        comparison_generator=comparison_generator
    )

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