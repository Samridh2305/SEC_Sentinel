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

