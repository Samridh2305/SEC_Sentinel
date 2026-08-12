import requests

from common.config import settings
from ingestion.sec_client import SECClient
from models.filing_metadata import DownloadedFiling, FilingMetadata


class FilingDownloader:

    def __init__(self, sec_client: SECClient):
        self.sec_client = sec_client

    def download_latest_filing(
        self,
        ticker: str,
        form_type: str
    )-> DownloadedFiling:

        cik = self.sec_client.get_company_cik(
            ticker
        )

        filing = self.sec_client.get_latest_filing(
            cik,
            form_type
        )

        accession_number = (
            filing["accessionNumber"]
            .replace("-", "")
        )
        primary_document = filing["primaryDocument"]

        url = (
            f"{settings.SEC_ARCHIVES_URL}"
            f"{int(cik)}/"
            f"{accession_number}/"
            f"{primary_document}"
        )

        response = requests.get(
            url,
            headers=self.sec_client.headers,
            timeout=30
        )

        response.raise_for_status()
        
        file_name = filing["primaryDocument"]

        settings.RAW_FILINGS_DIR.mkdir(
            parents=True,
            exist_ok=True
        )
        path = (
                settings.RAW_FILINGS_DIR /
                file_name
        )

        path.write_text(
            response.text,
            encoding="utf-8"
        )

        metadata = FilingMetadata(
            ticker=ticker,
            form_type=form_type,
            filing_date=filing["filingDate"],
            accession_number=filing["accessionNumber"]
        )

        return DownloadedFiling(
            path=path,
            metadata=metadata
        )