from typing import TypedDict


class AgentState(TypedDict):
    ticker:str
    form_type:str
    filing_date: str
    section: str | None
    query: str
    route: str | None
    answer: str | None
