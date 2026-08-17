from sqlalchemy.orm import Session

from db.models.ingestion_job import IngestionJob


class IngestionJobRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(
        self, ticker: str, form_type: str, filing_date: str | None
    ) -> IngestionJob:
        job = IngestionJob(
            ticker=ticker.upper(),
            form_type=form_type,
            requested_filing_date=filing_date,
        )
        self.session.add(job)
        self._commit()
        self.session.refresh(job)
        return job

    def get(self, job_id: str) -> IngestionJob | None:
        return self.session.get(IngestionJob, job_id)

    def mark_running(self, job: IngestionJob) -> None:
        job.status = "RUNNING"
        self._commit()

    def mark_completed(self, job: IngestionJob, result: dict) -> None:
        job.status = "COMPLETED"
        job.accession_number = result["accession_number"]
        job.chunks_created = result["chunks_created"]
        self._commit()

    def mark_failed(self, job: IngestionJob, error_message: str) -> None:
        job.status = "FAILED"
        job.error_message = error_message[:2000]
        self._commit()

    def _commit(self) -> None:
        try:
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
