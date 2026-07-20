from ingestion.sec_client import SECClient

client = SECClient()

def test_get_company_cik():
    assert client.get_company_cik("AAPL") == "0000320193"


def test_get_company_submissions():
    submissions = client.get_company_submissions("0000320193")

    assert "filings" in submissions
    assert "entityType" in submissions

def test_get_latest_filing():
    cik = client.get_company_cik("AAPL")

    filing = client.get_latest_filing(
        cik,
        "10-K"
    )

    assert "accessionNumber" in filing
    assert "filingDate" in filing
    assert "form" in filing
    assert "primaryDocument" in filing