import re
from collections import defaultdict


class SectionExtractor:

    SECTION_PATTERN = re.compile(
        r"Item\s+\d+[A-Z]?\.",
        re.IGNORECASE
    )

    def extract_sections(
        self,
        text: str
    ) -> dict[str, str]:

        matches = self._find_matches(text)

        real_matches = self._select_real_matches(matches)

        sections = self._slice_sections(
            text,
            real_matches
        )

        return sections

    def _find_matches(
        self,
        text: str
    ):

        return list(
            self.SECTION_PATTERN.finditer(text)
        )

    def _select_real_matches(
        self,
        matches
    ):

        groups = defaultdict(list)

        for match in matches:
            groups[match.group()].append(match)

        real_matches = []

        for section in sorted(groups):
            real_matches.append(
                groups[section][-1]
            )

        real_matches.sort(
            key=lambda match: match.start()
        )

        return real_matches

    def _slice_sections(
            self,
            text: str,
            matches
    ) -> dict[str, str]:

        sections = {}

        for i in range(len(matches)):

            current = matches[i]

            start = current.start()

            if i == len(matches) - 1:
                end = len(text)
            else:
                end = matches[i + 1].start()

            section_text = text[start:end]

            section_name = self.SECTION_NAMES.get(
                current.group(),
                current.group()
            )

            sections[section_name] = section_text.strip()

        return sections