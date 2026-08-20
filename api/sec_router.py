from fastapi import (
    APIRouter,
)

from ingestion.filing_downloader import FilingDownloader
from ingestion.sec_client import SECClient
from schema.schema import (
    FilingInfo,
)
from services.filing_service import FilingService

router = APIRouter(
    prefix="/sec/filings",
    tags=["SEC"]
)

sec_client = SECClient()

downloader = FilingDownloader(
    sec_client=sec_client
)


@router.get(
    "/available",
    response_model=list[FilingInfo]
)
def get_available_filings(
        ticker: str,
        form_type: str
):
    filing_service = FilingService(
        downloader=downloader,
        pipeline=None,
        sec_client=sec_client
    )

    return filing_service.get_available_filings(
        ticker=ticker,
        form_type=form_type
    )
