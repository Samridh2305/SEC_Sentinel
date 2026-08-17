from fastapi import APIRouter

from ingestion.sec_client import SECClient
from services.company_service import CompanyService
from schema.schema import CompanyResponse


router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


sec_client = SECClient()

company_service = CompanyService(
    sec_client=sec_client
)

@router.get(
    "/search",
    response_model=list[CompanyResponse]
)
def search_company(
    name: str
):
    return company_service.search_company(company_name=name)
