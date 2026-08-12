from dataclasses import dataclass
from pathlib import Path

@dataclass
class FilingMetadata:
    ticker: str
    form_type: str
    filing_date: str
    accession_number: str

@dataclass
class DownloadedFiling:
    path: Path
    metadata: FilingMetadata