from pathlib import Path

from ingestion.filing_downloader import FilingDownloader
from ingestion.sec_client import SECClient


def test_download_latest_filings():

    sec_client = SECClient()

    downloader = FilingDownloader(
        sec_client=sec_client
    )

    for form_type in [
        "10-K",
        "10-Q",
        "8-K"
    ]:

        path = downloader.download_latest_filing(
            ticker="AAPL",
            form_type=form_type
        )

        assert isinstance(path, Path)
        assert path.exists()
        assert path.stat().st_size > 0

