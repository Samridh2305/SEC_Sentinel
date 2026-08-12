from fastapi import APIRouter

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
    FilingDownloadResponse
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
    pipeline=pipeline
)

@router.post(
    "/download",
    response_model=FilingDownloadResponse
)
def download_filing(
    request: FilingDownloadRequest
):

    result = filing_service.download_and_ingest(
        ticker=request.ticker,
        form_type=request.form_type
    )

    return FilingDownloadResponse(
        **result,
        message="Filing downloaded and ingested successfully."
    )

