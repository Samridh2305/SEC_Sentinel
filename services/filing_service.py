class FilingService:

    def __init__(
        self,
        downloader,
        pipeline,
        sec_client
    ):
        self.downloader = downloader
        self.pipeline = pipeline
        self.sec_client = sec_client

    def download_and_ingest(
        self,
        ticker: str,
        form_type: str,
        filing_date:str |None=None
    ):
        if filing_date:

            downloaded_filing = (
                self.downloader.download_filing(
                    ticker=ticker,
                    form_type=form_type,
                    filing_date=filing_date
                )
            )

        else:

            downloaded_filing = (
                self.downloader.download_latest_filing(
                    ticker=ticker,
                    form_type=form_type
                )
            )

        chunks = self.pipeline.process_filing(
            filing_path=downloaded_filing.path,
            metadata=downloaded_filing.metadata
        )

        return {
            "ticker": downloaded_filing.metadata.ticker,
            "form_type": downloaded_filing.metadata.form_type,
            "filing_date": downloaded_filing.metadata.filing_date,
            "accession_number": downloaded_filing.metadata.accession_number,
            "chunks_created": len(chunks)
        }

    def get_available_filings(
            self,
            ticker: str,
            form_type: str
    ):
        return self.sec_client.get_all_filings(
            ticker=ticker,
            form_type=form_type
        )