from pydantic import BaseModel


class AnswerRequest(BaseModel):
    ticker: str
    form_type: str
    filing_date: str
    query: str

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

class FilingDownloadResponse(BaseModel):
    ticker: str
    form_type: str
    filing_date: str
    accession_number: str
    chunks_created: int
    message: str

class CompanyResponse(BaseModel):
    company: str
    ticker: str
    cik: str