import requests

from common.config import settings
from common.logger import logger
from exceptions.custom_exceptions import ProcessingException, ServiceException
from ingestion.sec_client import SECClient
from models.filing_metadata import DownloadedFiling, FilingMetadata


class FilingDownloader:

    def __init__(self, sec_client: SECClient):
        self.sec_client = sec_client

    def _download_text(self, url: str) -> str:
        try:
            response = requests.get(
                url, headers=self.sec_client.headers, timeout=30
            )
            response.raise_for_status()
            return response.text
        except requests.RequestException as exc:
            logger.exception("Could not download SEC filing from %s", url)
            raise ServiceException() from exc

    def _save_filing(self, file_name: str, text: str):
        try:
            settings.RAW_FILINGS_DIR.mkdir(parents=True, exist_ok=True)
            path = settings.RAW_FILINGS_DIR / file_name
            path.write_text(text, encoding="utf-8")
            return path
        except OSError as exc:
            logger.exception("Could not save downloaded filing %s", file_name)
            raise ProcessingException("Could not save the downloaded filing.") from exc

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

        file_name = filing["primaryDocument"]
        path = self._save_filing(file_name, self._download_text(url))

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

    def download_filing(
            self,
            ticker: str,
            form_type: str,
            filing_date: str
    ) -> DownloadedFiling:
        cik = self.sec_client.get_company_cik(
            ticker
        )

        filing = self.sec_client.get_filing(
            cik=cik,
            form_type=form_type,
            filing_date=filing_date
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

        # Include date to avoid overwriting another filing
        file_name = (
            f"{ticker.upper()}_"
            f"{form_type}_"
            f"{filing_date}_"
            f"{primary_document}"
        )

        path = self._save_filing(file_name, self._download_text(url))

        metadata = FilingMetadata(
            ticker=ticker.upper(),
            form_type=form_type,
            filing_date=filing["filingDate"],
            accession_number=filing["accessionNumber"]
        )

        return DownloadedFiling(
            path=path,
            metadata=metadata
        )
