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


def test_extract_sections():

    parser = FilingParser()
    extractor = SectionExtractor()

    soup = parser.parse(
        Path("data/raw/filings/aapl-20250927.htm")
    )

    soup = parser.clean(soup)

    text = parser.extract_visible_text(soup)

    sections = extractor.extract_sections(text)

    print(sections.keys())

    assert "Item 1." in sections
    assert "Item 1A." in sections
    assert "Item 7." in sections