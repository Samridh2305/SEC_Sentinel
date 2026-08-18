from datetime import datetime

from db.repositories.filing_chunk_repository import FilingChunkRepository
from exceptions.custom_exceptions import BadRequestException, NotFoundException
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
            section: str | None,
            query: str,
            comparison_filing_date: str | None = None,
    ):
        if comparison_filing_date:
            self._validate_comparison_dates(
                filing_date=filing_date,
                comparison_filing_date=comparison_filing_date,
            )
            previous_chunks = self.repository.get_chunks(
                ticker=ticker,
                form_type=form_type,
                filing_date=comparison_filing_date,
                section=section,
            )
            if not previous_chunks:
                raise NotFoundException(
                    "The selected comparison filing was not found."
                )
        else:
            previous_filing = self.repository.get_previous_filing(
                ticker=ticker,
                form_type=form_type,
                filing_date=filing_date,
            )
            if previous_filing is None:
                raise NotFoundException("No previous filing found.")
            previous_chunks = self.repository.get_chunks(
                ticker=ticker,
                form_type=form_type,
                filing_date=str(previous_filing["filing_date"]),
                section=section,
            )

        current_chunks = self.repository.get_chunks(
            ticker=ticker,
            form_type=form_type,
            filing_date=filing_date,
            section=section,
        )
        if not current_chunks:
            raise NotFoundException("The selected current filing was not found.")

        return self.comparison_generator.generate_comparison(
            query=query,
            section=section,
            previous_chunks=previous_chunks,
            current_chunks=current_chunks
        )

    @staticmethod
    def _validate_comparison_dates(
            filing_date: str,
            comparison_filing_date: str,
    ) -> None:
        try:
            current_date = datetime.strptime(filing_date, "%Y-%m-%d").date()
            comparison_date = datetime.strptime(
                comparison_filing_date, "%Y-%m-%d"
            ).date()
        except ValueError as exc:
            raise BadRequestException("Dates must use YYYY-MM-DD format.") from exc

        if comparison_date >= current_date:
            raise BadRequestException(
                "The comparison filing date must be earlier than the current filing date."
            )
