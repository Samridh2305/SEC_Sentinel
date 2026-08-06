from pathlib import Path

import pytest

from extraction.filing_parser import FilingParser
from extraction.section_extractor import SectionExtractor
from extraction.xbrl_cleaner import XBRLCleaner


parser = FilingParser()
cleaner = XBRLCleaner()
extractor = SectionExtractor()

FILING_PATH = Path("data/raw/filings/aapl-20250927.htm")


@pytest.fixture
def soup():
    return parser.parse(FILING_PATH)


@pytest.fixture
def cleaned_soup(soup):
    return parser.clean(soup)


@pytest.fixture
def filing_text(cleaned_soup):
    return parser.extract_visible_text(cleaned_soup)


def test_clean(cleaned_soup, soup):
    assert cleaned_soup is soup


def test_extract_visible_text(filing_text):
    assert isinstance(filing_text, str)
    assert len(filing_text) > 0


def test_extract_sections(filing_text):

    cleaned_text = cleaner.clean_text(
        text=filing_text,
        company_name="Apple Inc.",
        form_type="10-K",
        filing_year=2025
    )

    sections = extractor.extract_sections(
        cleaned_text
    )

    assert "Business" in sections

    assert "Risk Factors" in sections

    assert (
        "Management Discussion and Analysis"
        in sections
    )

    assert "Financial Statements" in sections