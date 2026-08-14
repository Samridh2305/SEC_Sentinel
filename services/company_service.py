from ingestion.sec_client import SECClient


class CompanyService:

    def __init__(
        self,
        sec_client: SECClient
    ):
        self.sec_client = sec_client

    def search_company(
        self,
        company_name: str
    ):

        results = self.sec_client.search_company(
            company_name
        )

        if not results:
            raise ValueError(
                f"No SEC company found matching "
                f"'{company_name}'."
            )

        return results