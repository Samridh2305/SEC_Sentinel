from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    status,
)
from sqlalchemy.orm import Session

from db.database import get_db
from db.repositories.filing_chunk_repository import FilingChunkRepository
from db.repositories.ingestion_job_repository import IngestionJobRepository
from exceptions.custom_exceptions import NotFoundException
from ingestion.filing_downloader import FilingDownloader
from ingestion.sec_client import SECClient
from schema.schema import (
    FilingDownloadRequest,
    IngestionJobResponse, FilingItem,
)
from schema.schema import FilingResponse
from services.ingestion_job_worker import run_ingestion_job

router = APIRouter(
    prefix="/filings",
    tags=["Filings"],
)

sec_client = SECClient()

downloader = FilingDownloader(
    sec_client=sec_client
)


@router.get(
    "/available",
    response_model=FilingResponse,
)
def get_all_filings(
    ticker: str,
    form_type: str,
    db: Session = Depends(get_db),
):
    repository = FilingChunkRepository(db)

    filings = repository.get_available_filings_in_db(
        ticker=ticker,
        form_type=form_type,
    )

    return FilingResponse(
        ticker=ticker,
        form_type=form_type,
        filings=[
            FilingItem(
                filing_date=filing.filing_date,
                accession_number=filing.accession_number,
            )
            for filing in filings
        ],
    )


@router.post(
    "/download",
    response_model=IngestionJobResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
def download_filing(
    request: FilingDownloadRequest,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_db)
):
    jobs = IngestionJobRepository(session)
    job = jobs.create(
        ticker=request.ticker,
        form_type=request.form_type,
        filing_date=request.filing_date,
    )

    background_tasks.add_task(run_ingestion_job, job.id)

    return IngestionJobResponse(
        job_id=job.id,
        status=job.status,
        ticker=job.ticker,
        form_type=job.form_type,
        requested_filing_date=job.requested_filing_date,
    )


@router.get(
    "/jobs/{job_id}",
    response_model=IngestionJobResponse,
)
def get_ingestion_job(
    job_id: str,
    session: Session = Depends(get_db),
):
    job = IngestionJobRepository(session).get(job_id)

    if job is None:
        raise NotFoundException("Ingestion job not found.")

    return IngestionJobResponse(
        job_id=job.id,
        status=job.status,
        ticker=job.ticker,
        form_type=job.form_type,
        requested_filing_date=job.requested_filing_date,
        accession_number=job.accession_number,
        chunks_created=job.chunks_created,
        error_message=job.error_message,
    )