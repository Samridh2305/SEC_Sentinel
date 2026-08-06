from pathlib import Path
from bs4 import BeautifulSoup

from extraction.filing_parser import FilingParser


parser = FilingParser()

def test_extract_text():

    soup = parser.parse(
        Path("data/raw/filings/aapl-20250927.htm")
    )

    text = parser.extract_text(soup)

    assert isinstance(text, str)

    assert len(text) > 0
    print(text[:3000])

def test_parse():
    soup = parser.parse(
        Path("data/raw/filings/aapl-20250927.htm")
    )

    assert isinstance(soup, BeautifulSoup)