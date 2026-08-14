from fastapi import (
    APIRouter,
    HTTPException
)

from db.database import SessionLocal
from db.repositories.filing_chunk_repository import (
    FilingChunkRepository
)

from ingestion.sec_client import SECClient
from ingestion.filing_downloader import FilingDownloader
from ingestion.ingestion_pipeline import IngestionPipeline

from extraction.filing_parser import FilingParser
from extraction.section_extractor import SectionExtractor
from ingestion.chunker import Chunker
from embeddings.embedder import Embedder

from services.filing_service import FilingService

from schema.schema import (
    FilingDownloadRequest,
    FilingDownloadResponse, FilingInfo
)

router = APIRouter(
    prefix="/filings",
    tags=["Filings"]
)

session = SessionLocal()

sec_client = SECClient()

downloader = FilingDownloader(
    sec_client=sec_client
)

parser = FilingParser()

section_extractor = SectionExtractor()

chunker = Chunker()

embedder = Embedder()

repository = FilingChunkRepository(
    session=session
)

pipeline = IngestionPipeline(
    parser=parser,
    section_extractor=section_extractor,
    chunker=chunker,
    embedder=embedder,
    repository=repository
)

filing_service = FilingService(
    downloader=downloader,
    pipeline=pipeline,
    sec_client=sec_client
)

@router.post(
    "/download",
    response_model=FilingDownloadResponse
)
def download_filing(
    request: FilingDownloadRequest
):

    try:

        result = filing_service.download_and_ingest(
            ticker=request.ticker,
            form_type=request.form_type,
            filing_date=request.filing_date
        )

        return FilingDownloadResponse(
            **result,
            message="Filing downloaded and ingested successfully."
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

@router.get(
    "/available",
    response_model=list[FilingInfo]
)
def get_available_filings(
    ticker: str,
    form_type: str
):

    try:

        return filing_service.get_available_filings(
            ticker=ticker,
            form_type=form_type
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )