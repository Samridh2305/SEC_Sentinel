from collections import defaultdict

from exceptions.custom_exceptions import BadRequestException
from models.section_match import SectionMatch
from services.classes import FORM_CONFIG, PART_PATTERN


class SectionExtractor:

    def _get_filing_config(
            self,
            form_type: str
    ):
        config = FORM_CONFIG.get(form_type)
        if config is None:
            raise BadRequestException(
                f"Unsupported form type: {form_type}"
            )
        return config

    def extract_sections(
        self,
        text: str,
        form_type:str
    ) -> dict[str, str]:

        config=self._get_filing_config(form_type)

        pattern=config["pattern"]
        section_names=config["sections"]

        matches = self._find_matches(text,pattern,form_type)

        real_matches = self._select_real_matches(
            matches
        )

        sections = self._slice_sections(
            text,
            real_matches,
            section_names
        )

        return sections

    def _find_matches(
            self,
            text: str,
            pattern,
            form_type: str
    ):
        # 10-K and 8-K
        if form_type != "10-Q":

            matches = []

            for match in pattern.finditer(text):
                matches.append(
                    SectionMatch(
                        match=match,
                        lookup_key=match.group().lower()
                    )
                )

            return matches

        # 10-Q
        current_part = None

        part_matches = list(
            PART_PATTERN.finditer(text)
        )

        item_matches = list(
            pattern.finditer(text)
        )

        events = []

        # Add PART headings
        for match in part_matches:
            events.append(
                ("part", match)
            )

        # Add ITEM headings
        for match in item_matches:
            events.append(
                ("item", match)
            )

        # Sort by position in document
        events.sort(
            key=lambda event: event[1].start()
        )

        matches = []

        for event_type, match in events:

            if event_type == "part":
                current_part = match.group().lower()
                continue

            lookup_key = (
                f"{current_part} {match.group().lower()}"
            )

            matches.append(
                SectionMatch(
                    match=match,
                    lookup_key=lookup_key
                )
            )

        return matches

    def _select_real_matches(
        self,
        matches
    ):

        groups = defaultdict(list)

        for match in matches:

            normalized_section = (
                match.lookup_key
            )

            groups[normalized_section].append(match)

        real_matches = []

        for section in sorted(groups):

            real_matches.append(
                groups[section][-1]
            )

        real_matches.sort(
            key=lambda match: match.match.start()
        )

        return real_matches

    def _slice_sections(
        self,
        text: str,
        matches,
        section_names
    ):

        sections = {}

        for i in range(len(matches)):

            current = matches[i]

            start = current.match.start()

            if i == len(matches) - 1:
                end = len(text)
            else:
                end = matches[i + 1].match.start()

            section_text = text[start:end]

            section_name = section_names.get(
                current.lookup_key,
                current.match.group().strip()
            )

            sections[section_name] = section_text.strip()

        return sections
