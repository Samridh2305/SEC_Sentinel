
from pathlib import Path

from db.database import SessionLocal
from db.models.filing_chunk import FilingChunk
from db.repositories.filing_chunk_repository import (
    FilingChunkRepository
)

from extraction.filing_parser import FilingParser
from extraction.section_extractor import SectionExtractor

from ingestion.chunker import Chunker
from ingestion.ingestion_pipeline import IngestionPipeline

from embeddings.embedder import Embedder

from models.filing_metadata import FilingMetadata


def test_full_ingestion_pipeline():

    # 1. Create components

    parser = FilingParser()

    section_extractor = SectionExtractor()

    chunker = Chunker()

    embedder = Embedder()


    # 2. Create database session

    session = SessionLocal()


    try:

        # 3. Create repository

        repository = FilingChunkRepository(
            session
        )


        # 4. Create pipeline

        pipeline = IngestionPipeline(

            parser=parser,

            section_extractor=section_extractor,

            chunker=chunker,

            embedder=embedder,

            repository=repository
        )


        # 5. Filing metadata

        metadata = FilingMetadata(

            ticker="AAPL",

            form_type="10-K",

            filing_date="2025-09-27",

            accession_number="YOUR_ACCESSION_NUMBER"
        )


        # 6. Run pipeline

        chunks = pipeline.process_filing(

            filing_path=Path(
                "data/raw/filings/"
                "aapl-20250927.htm"
            ),

            metadata=metadata
        )


        # 7. Verify chunks were created

        assert len(chunks) > 0


        # 8. Verify embeddings exist

        for chunk in chunks:

            assert chunk.embedding is not None

            assert len(
                chunk.embedding
            ) == 768


        # 9. Verify database insertion

        saved_chunks = (

            session.query(FilingChunk)

            .filter(

                FilingChunk.ticker == "AAPL",

                FilingChunk.form_type == "10-K",

                FilingChunk.accession_number
                == "YOUR_ACCESSION_NUMBER"

            )

            .all()
        )


        # 10. Verify database contains chunks

        assert len(
            saved_chunks
        ) == len(chunks)


        # 11. Verify Risk Factors exist

        risk_chunks = [

            chunk

            for chunk in saved_chunks

            if chunk.section
            == "Risk Factors"
        ]


        assert len(
            risk_chunks
        ) > 0


    finally:

        session.close()

