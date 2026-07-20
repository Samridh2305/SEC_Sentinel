from bs4 import BeautifulSoup


class XBRLCleaner:

    def clean(
        self,
        soup: BeautifulSoup
    ) -> BeautifulSoup:

        return soup

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
            raise ValueError(
                "No <body> found."
            )

        lines = []

        for text in body.stripped_strings:
            lines.append(text)

        return "\n".join(lines)