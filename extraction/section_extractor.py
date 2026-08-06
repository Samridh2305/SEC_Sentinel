import re
from collections import defaultdict


class SectionExtractor:

    SECTION_PATTERN = re.compile(
        r"\bItem\s+\d+[A-Z]?\.",
        re.IGNORECASE
    )

    SECTION_NAMES = {
        "item 1.": "Business",
        "item 1a.": "Risk Factors",
        "item 1b.": "Unresolved Staff Comments",
        "item 1c.": "Cybersecurity",
        "item 2.": "Properties",
        "item 3.": "Legal Proceedings",
        "item 4.": "Mine Safety Disclosures",
        "item 5.": "Market for Registrant's Common Equity",
        "item 6.": "Selected Financial Data",
        "item 7.": "Management Discussion and Analysis",
        "item 7a.": "Market Risk",
        "item 8.": "Financial Statements",
        "item 9.": "Changes in Accountants",
        "item 9a.": "Controls and Procedures",
        "item 9b.": "Other Information",
        "item 9c.": "Foreign Jurisdictions",
        "item 10.": "Directors and Executive Officers",
        "item 11.": "Executive Compensation",
        "item 12.": "Security Ownership",
        "item 13.": "Related Party Transactions",
        "item 14.": "Principal Accounting Fees",
        "item 15.": "Exhibits",
        "item 16.": "Form 10-K Summary",
    }

    def extract_sections(
        self,
        text: str
    ) -> dict[str, str]:

        matches = self._find_matches(text)

        real_matches = self._select_real_matches(
            matches
        )

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

            normalized_section = (
                match.group().lower()
            )

            groups[
                normalized_section
            ].append(match)

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

                end = matches[
                    i + 1
                ].start()

            section_text = text[
                start:end
            ]

            normalized_section = (
                current.group().lower()
            )

            section_name = (
                self.SECTION_NAMES.get(
                    normalized_section,
                    current.group().strip()
                )
            )

            sections[
                section_name
            ] = section_text.strip()

        return sections