from datetime import datetime

from sqlalchemy.orm import Session

from db.models.filing_chunk import FilingChunk
from models.chunk import Chunk


class FilingChunkRepository:

    def __init__(self, session: Session):
        self.session = session

    def save_chunks(
        self,
        chunks: list[Chunk]
    ) -> None:

        filing_chunks = []

        for chunk in chunks:

            filing_chunk = FilingChunk(
                ticker=chunk.ticker,
                form_type=chunk.form_type,
                filing_date=datetime.strptime(chunk.filing_date,"%Y-%m-%d").date(),
                accession_number=chunk.accession_number,
                section=chunk.section,
                chunk_index=chunk.chunk_index,
                text=chunk.text,
                embedding=chunk.embedding
            )

            filing_chunks.append(
                filing_chunk
            )

        self.session.add_all(
            filing_chunks
        )

        self.session.commit()

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
