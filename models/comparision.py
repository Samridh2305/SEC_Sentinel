from dataclasses import dataclass

from db.models.filing_chunk import FilingChunk


@dataclass
class Comparison:
    text: str
    current_sources: list[FilingChunk]
    previous_sources: list[FilingChunk]