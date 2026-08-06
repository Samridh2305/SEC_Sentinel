from dataclasses import dataclass

from db.models.filing_chunk import FilingChunk


@dataclass
class Answer:

    text: str

    sources: list[FilingChunk]