from dataclasses import dataclass


@dataclass
class Chunk:

    id: str

    ticker: str

    form_type: str

    filing_date: str

    accession_number: str

    section: str

    chunk_index: int

    text: str

    embedding: list[float] | None = None