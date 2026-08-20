from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from common.logger import logger
from db.models.filing_chunk import FilingChunk
from exceptions.custom_exceptions import DatabaseException
from models.chunk import Chunk


class FilingChunkRepository:

    def __init__(self, session: Session):
        self.session = session

    def save_chunks(
        self,
        chunks: list[Chunk]
    ) -> int:
        """Save chunks once; repeated ingestion skips existing chunks."""
        if not chunks:
            return 0

        rows = [
            {
                "ticker": chunk.ticker,
                "form_type": chunk.form_type,
                "filing_date": datetime.strptime(
                    chunk.filing_date, "%Y-%m-%d"
                ).date(),
                "accession_number": chunk.accession_number,
                "section": chunk.section,
                "chunk_index": chunk.chunk_index,
                "text": chunk.text,
                "embedding": chunk.embedding,
            }
            for chunk in chunks
        ]

        try:
            statement = insert(FilingChunk).values(rows)
            statement = statement.on_conflict_do_nothing(
                constraint="uq_filing_chunks_accession_section_index"
            )
            result = self.session.execute(statement)
            self.session.commit()
            return result.rowcount or 0
        except Exception as exc:
            self.session.rollback()
            logger.exception("Could not save filing chunks")
            raise DatabaseException() from exc

    def filing_exists(self, accession_number: str) -> bool:
        return (
            self.session.query(FilingChunk.id)
            .filter(FilingChunk.accession_number == accession_number)
            .first()
            is not None
        )

    def get_available_filings_in_db(
            self,
            ticker: str | None = None,
            form_type: str | None = None,
    ):
        query = (
            self.session.query(
                FilingChunk.ticker,
                FilingChunk.form_type,
                FilingChunk.filing_date,
                FilingChunk.accession_number,
            )
            .distinct()
        )

        if ticker:
            query = query.filter(
                FilingChunk.ticker == ticker
            )

        if form_type:
            query = query.filter(
                FilingChunk.form_type == form_type
            )

        return query.order_by(
            FilingChunk.filing_date.desc()
        ).all()

    def get_chunks(
            self,
            ticker: str,
            form_type: str,
            filing_date: str,
            section: str | None = None
    ) -> list[FilingChunk]:

        query = (
            self.session.query(FilingChunk)
        )
        query = query.filter(
            FilingChunk.ticker == ticker,
            FilingChunk.form_type == form_type,
            FilingChunk.filing_date == datetime.strptime(
                filing_date,
                "%Y-%m-%d"
            ).date(),
        )

        if section:
            query = query.filter(
                FilingChunk.section == section
            )

        query = query.order_by(
            FilingChunk.chunk_index
        )

        return query.all()


    def get_previous_filing(
        self,
        ticker: str,
        form_type: str,
        filing_date: str
    ):
        current_date = datetime.strptime(
            filing_date,
            "%Y-%m-%d"
        ).date()

        query = self.session.query(FilingChunk)

        query=query.filter(
        FilingChunk.ticker==ticker,
        FilingChunk.form_type == form_type
        )

        query = query.filter(
            FilingChunk.filing_date < current_date
        )

        query = query.order_by(
            FilingChunk.filing_date.desc()
        )

        result= (query.with_entities(
            FilingChunk.filing_date,
            FilingChunk.accession_number
        )
        .distinct()
        .first()
        )
        
        if result is None:
            return None

        return {
            "filing_date": result.filing_date,
            "accession_number": result.accession_number,
        }
