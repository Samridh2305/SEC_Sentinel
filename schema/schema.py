from typing import Literal

from pydantic import BaseModel


class AnswerRequest(BaseModel):
    ticker: str
    form_type: str
    filing_date: str
    query: str
    section: str | None = None

class AnswerResponse(BaseModel):
    answer:str

class ComparisonRequest(BaseModel):
    ticker: str
    form_type: str
    filing_date: str
    section: str
    query: str

class ComparisonResponse(BaseModel):
    comparison: str

class FilingDownloadRequest(BaseModel):
    ticker: str
    form_type: str
    filing_date: str | None = None

class FilingInfo(BaseModel):
    form_type: str
    filing_date: str
    accession_number: str
    primary_document: str

class FilingDownloadResponse(BaseModel):
    ticker: str
    form_type: str
    filing_date: str
    accession_number: str
    chunks_created: int
    message: str


class IngestionJobResponse(BaseModel):
    job_id: str
    status: str
    ticker: str
    form_type: str
    requested_filing_date: str | None
    accession_number: str | None = None
    chunks_created: int | None = None
    error_message: str | None = None

class CompanyResponse(BaseModel):
    company: str
    ticker: str
    cik: str

class RouteDecision(BaseModel):
    route: Literal["ANSWER", "COMPARISON"]
