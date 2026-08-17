import re

from bs4 import BeautifulSoup

from exceptions.custom_exceptions import ProcessingException


class XBRLCleaner:

    def clean(
        self,
        soup: BeautifulSoup
    ) -> BeautifulSoup:

        return soup

    def clean_text(self, text: str, company_name: str, form_type: str,
                   filing_year: int
                   ) -> str:

        page_header_pattern = re.compile(
            rf"{re.escape(company_name)}"
            rf"\s*\|\s*" rf"{filing_year}" 
            rf"\s+Form\s+{re.escape(form_type)}"
            rf"\s*\|\s*\d+", re.IGNORECASE
        )

        text = page_header_pattern.sub( "", text )

        text = re.sub(
            r"[ \t]+", " ", text
        )
        text = re.sub(
            r"\n\s*\n+", "\n\n", text
        )

        return text.strip()

    def inspect_tags(
            self,
            soup: BeautifulSoup
    ):
        tags = set()

        for tag in soup.find_all():
            tags.add(tag.name)

        return sorted(tags)

    def extract_visible_text(
            self,
            soup: BeautifulSoup
    ) -> str:

        body = soup.body

        if body is None:
            raise ProcessingException(
                "No <body> found."
            )

        lines = []

        for text in body.stripped_strings:
            lines.append(text)

        return "\n".join(lines)
