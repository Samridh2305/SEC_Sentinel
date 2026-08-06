from pathlib import Path

from extraction.filing_parser import FilingParser
from extraction.section_extractor import SectionExtractor
from ingestion.chunker import Chunker
from models.filing_metadata import FilingMetadata
from embeddings.embedder import Embedder


def test_embed_aapl_filing():
    # 1. Parse filing
    parser = FilingParser()

    soup = parser.parse(
        Path(
            "data/raw/filings/"
            "aapl-20250927.htm"
        )
    )

    # 2. Extract visible text
    text = parser.extract_visible_text(
        soup
    )

    # 3. Extract sections
    section_extractor = SectionExtractor()

    sections = section_extractor.extract_sections(
        text
    )

    # 4. Create metadata
    metadata = FilingMetadata(
        ticker="AAPL",
        form_type="10-K",
        filing_date="2025-09-27",
        accession_number="YOUR_ACCESSION_NUMBER"
    )

    # 5. Chunk sections
    chunker = Chunker()

    chunks = chunker.chunk_sections(
        sections=sections,
        metadata=metadata
    )

    # 6. Create embedder
    embedder = Embedder()

    # 7. Generate embeddings
    embedded_chunks = embedder.embed_chunks(
        chunks
    )

    # 8. Check number of chunks
    assert len(embedded_chunks) == len(chunks)

    assert len(embedded_chunks) > 0

    # 9. Check every Chunk
    for chunk in embedded_chunks:
        # Verify it is a Chunk
        assert chunk.embedding is not None

        # Verify embedding is a list
        assert isinstance(
            chunk.embedding,
            list
        )

        # Verify embedding has 768 dimensions
        assert len(
            chunk.embedding
        ) == 768

        # Verify every value is a float
        assert all(
            isinstance(value, float)
            for value in chunk.embedding
        )