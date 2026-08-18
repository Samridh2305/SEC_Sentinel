from typing import TypedDict


class AgentState(TypedDict):
    ticker:str
    form_type:str
    filing_date: str
    comparison_filing_date: str | None
    section: str | None
    query: str
    route: str | None
    answer: str | None
