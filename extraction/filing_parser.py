from pathlib import Path
from bs4 import BeautifulSoup

class FilingParser:

    def parse(
        self,
        filing_path: Path
    )-> BeautifulSoup:

        html= filing_path.read_text(encoding="utf-8")

        soup = BeautifulSoup(html, "html.parser")

        return soup

    def clean(
            self,
            soup: BeautifulSoup
    ) -> BeautifulSoup:

        for tag in soup(
                [
                    "script",
                    "style",
                    "meta",
                    "link"
                ]
        ):
            tag.decompose()

        return soup

    def extract_visible_text(
            self,
            soup: BeautifulSoup
    ) -> str:

        body = soup.body

        if body is None:
            raise ValueError(
                "No <body> found."
            )

        lines = []

        for text in body.stripped_strings:
            lines.append(text)

        return "\n".join(lines)

    
    def extract_sections(self, soup:BeautifulSoup)-> str:

        return soup.get_text(
            separator="\n",
            strip=True
        )