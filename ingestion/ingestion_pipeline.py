from pathlib import Path

from extraction.filing_parser import FilingParser
from extraction.section_extractor import SectionExtractor
from ingestion.chunker import Chunker
from embeddings.embedder import Embedder
from db.repositories.filing_chunk_repository import (
    FilingChunkRepository
)
from common.logger import logger
from exceptions.custom_exceptions import ProcessingException
from models.filing_metadata import FilingMetadata


class IngestionPipeline:

    def __init__(
        self,
        parser: FilingParser,
        section_extractor: SectionExtractor,
        chunker: Chunker,
        embedder: Embedder,
        repository: FilingChunkRepository
    ):
        self.parser = parser
        self.section_extractor = section_extractor
        self.chunker = chunker
        self.embedder = embedder
        self.repository = repository

    def process_filing(
        self,
        filing_path: Path,
        metadata: FilingMetadata
    ):

        # 1. Parse HTML/XBRL filing
        soup = self.parser.parse(
            filing_path
        )

        # 2. Clean filing
        soup = self.parser.clean(
            soup
        )

        # 3. Extract visible text
        text = self.parser.extract_visible_text(
            soup
        )

        # 4. Extract SEC sections
        sections = (
            self.section_extractor
            .extract_sections(text=text,form_type=metadata.form_type)
        )
        if not sections:
            logger.error(
                "No sections extracted for %s filing %s",
                metadata.form_type,
                metadata.accession_number,
            )
            raise ProcessingException(
                "No recognized sections were found in the filing."
            )

        # 5. Split sections into chunks
        chunks = self.chunker.chunk_sections(
            sections=sections,
            metadata=metadata
        )
        if not chunks:
            logger.error(
                "No chunks created for filing %s",
                metadata.accession_number,
            )
            raise ProcessingException("No chunks could be created from the filing.")

        # 6. Generate embeddings
        chunks = self.embedder.embed_chunks(
            chunks
        )

        # 7. Save chunks to PostgreSQL
        self.repository.save_chunks(
            chunks
        )

        return chunks
