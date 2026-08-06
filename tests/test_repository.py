from db.database import SessionLocal
from db.models.filing_chunk import FilingChunk
from db.repositories.filing_chunk_repository import (
    FilingChunkRepository
)
from models.chunk import Chunk


def test_save_chunk():

    chunk = Chunk(
        id="test_chunk_1",
        ticker="AAPL",
        form_type="10-K",
        filing_date="2025-09-27",
        accession_number="TEST_ACCESSION",
        section="Risk Factors",
        chunk_index=0,
        text="Apple faces various business risks.",
        embedding=[0.1] * 768
    )

    session = SessionLocal()

    try:

        repository = FilingChunkRepository(
            session
        )

        repository.save_chunks(
            [chunk]
        )

        saved_chunk = (
            session.query(FilingChunk)
            .filter(
                FilingChunk.ticker == "AAPL",
                FilingChunk.accession_number
                == "TEST_ACCESSION"
            )
            .first()
        )

        assert saved_chunk is not None

        assert saved_chunk.ticker == "AAPL"

        assert saved_chunk.form_type == "10-K"

        assert saved_chunk.section == "Risk Factors"

        assert saved_chunk.chunk_index == 0

        assert (
            saved_chunk.text
            == "Apple faces various business risks."
        )

        assert len(
            saved_chunk.embedding
        ) == 768

    finally:

        session.close()

