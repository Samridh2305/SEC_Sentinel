from common.logger import logger
from db.database import SessionLocal
from db.repositories.filing_chunk_repository import FilingChunkRepository
from db.repositories.ingestion_job_repository import IngestionJobRepository
from embeddings.embedder import Embedder
from extraction.filing_parser import FilingParser
from extraction.section_extractor import SectionExtractor
from ingestion.chunker import Chunker
from ingestion.filing_downloader import FilingDownloader
from ingestion.ingestion_pipeline import IngestionPipeline
from ingestion.sec_client import SECClient
from services.filing_service import FilingService


sec_client = SECClient()

downloader = FilingDownloader(sec_client=sec_client)

parser = FilingParser()
section_extractor = SectionExtractor()
chunker = Chunker()
embedder = Embedder()


def run_ingestion_job(job_id: str) -> None:
    """Process one job using a task-owned database session."""
    session = SessionLocal()
    jobs = IngestionJobRepository(session)

    try:
        job = jobs.get(job_id)
        if job is None:
            logger.error("Ingestion job %s was not found", job_id)
            return

        jobs.mark_running(job)

        repository = FilingChunkRepository(session)
        pipeline = IngestionPipeline(
            parser=parser,
            section_extractor=section_extractor,
            chunker=chunker,
            embedder=embedder,
            repository=repository,
        )
        filing_service = FilingService(
            downloader=downloader,
            pipeline=pipeline,
            sec_client=sec_client,
        )

        result = filing_service.download_and_ingest(
            ticker=job.ticker,
            form_type=job.form_type,
            filing_date=job.requested_filing_date,
        )
        jobs.mark_completed(job, result)

    except Exception as exc:
        logger.exception("Ingestion job %s failed", job_id)
        job = jobs.get(job_id)
        if job is not None:
            try:
                jobs.mark_failed(job, str(exc))
            except Exception:
                logger.exception("Could not record failure for job %s", job_id)
    finally:
        session.close()
