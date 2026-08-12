from pathlib import Path

from extraction.filing_parser import FilingParser
from extraction.section_extractor import SectionExtractor
from ingestion.chunker import Chunker
from models.filing_metadata import FilingMetadata


def test_chunk_aapl_filing():

    # 1. Parse filing
    parser = FilingParser()

    soup = parser.parse(
        Path(
            "data/raw/filings/"
            "aapl-20250927.htm"
        )
    )

    # 2. Extract visible text
    text = parser.extract_visible_text(soup)

    # 3. Extract sections
    section_extractor = SectionExtractor()

    sections = (
        section_extractor.extract_sections(text)
    )

    # 4. Create filing metadata
    metadata = FilingMetadata(
        ticker="AAPL",
        form_type="10-K",
        filing_date="2025-09-27",
        accession_number="YOUR_ACCESSION_NUMBER"
    )

    # 5. Create chunker
    chunker = Chunker()

    # 6. Create chunks
    chunks = chunker.chunk_sections(
        sections=sections,
        metadata=metadata
    )

    # 7. Basic assertions
    assert len(chunks) > 0

    # 8. Check Risk Factors chunks
    risk_chunks = [
        chunk
        for chunk in chunks
        if chunk.section == "Risk Factors"
    ]

    assert len(risk_chunks) > 0

