class FilingService:

    def __init__(
        self,
        downloader,
        pipeline
    ):
        self.downloader = downloader
        self.pipeline = pipeline

    def download_and_ingest(
        self,
        ticker: str,
        form_type: str
    ):

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