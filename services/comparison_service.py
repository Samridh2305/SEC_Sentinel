
from db.repositories.filing_chunk_repository import FilingChunkRepository
from generation.comparison_generator import ComparisonGenerator


class ComparisonService:

    def __init__(
        self,
        repository: FilingChunkRepository,
        comparison_generator: ComparisonGenerator
    ):
        self.repository = repository
        self.comparison_generator = comparison_generator

    def compare(
            self,
            ticker: str,
            form_type: str,
            filing_date: str,
            section: str,
            query: str
    ):
        previous_filing = (
            self.repository.get_previous_filing(
                ticker=ticker,
                form_type=form_type,
                filing_date=filing_date
            )
        )
        if previous_filing is None:
            raise ValueError(
                "No previous filing found."
            )
        previous_chunks = (
            self.repository.get_chunks(
                ticker=ticker,
                form_type=form_type,
                filing_date=str(
                    previous_filing["filing_date"]
                ),
                section=section
            )
        )
        current_chunks = (
            self.repository.get_chunks(
                ticker=ticker,
                form_type=form_type,
                filing_date=filing_date,
                section=section
            )
        )
        return self.comparison_generator.generate_comparison(
            query=query,
            previous_chunks=previous_chunks,
            current_chunks=current_chunks
        )