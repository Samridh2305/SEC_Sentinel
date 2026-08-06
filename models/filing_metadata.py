from dataclasses import dataclass


@dataclass
class FilingMetadata:
    ticker: str
    form_type: str
    filing_date: str
    accession_number: str
