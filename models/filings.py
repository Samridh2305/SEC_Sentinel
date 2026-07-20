from dataclasses import dataclass


@dataclass
class Filing:

    ticker: str

    form_type: str

    filing_date: str

    accession_number: str

    sections: dict[str, str]