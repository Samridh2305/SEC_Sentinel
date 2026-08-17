from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    status,
)
from sqlalchemy.orm import Session

from db.database import get_db
from db.repositories.ingestion_job_repository import IngestionJobRepository
from ingestion.filing_downloader import FilingDownloader
from ingestion.sec_client import SECClient
from schema.schema import (
    FilingDownloadRequest,
    FilingInfo,
    IngestionJobResponse,
)
from services.filing_service import FilingService
from services.ingestion_job_worker import run_ingestion_job
from exceptions.custom_exceptions import NotFoundException

router = APIRouter(
    prefix="/filings",
    tags=["Filings"]
)

sec_client = SECClient()

downloader = FilingDownloader(
    sec_client=sec_client
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
