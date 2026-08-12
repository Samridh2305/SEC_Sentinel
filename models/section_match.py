import re
from dataclasses import dataclass


@dataclass
class SectionMatch:
    match: re.Match
    lookup_key: str