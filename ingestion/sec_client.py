import requests

from common.config import settings


class SECClient:

    def __init__(self):
        self.headers = {
            "User-Agent": "Samridh samridh2305@gmail.com"
        }
        self.companies =self._load_companies()

    def _load_companies(self) -> dict:

        response = requests.get(
            settings.SEC_COMPANY_TICKERS_URL,
            headers=self.headers,
            timeout=30
        )
        response.raise_for_status()

        return response.json()

    def get_company_cik(self, ticker: str) -> str:

        ticker = ticker.upper()

        for company in self.companies.values():

            if company["ticker"] == ticker:

                cik = str(company["cik_str"])

                return cik.zfill(10) #SEC expects 10 digits so her we fill remaining digits with zero

        raise ValueError(f"Ticker {ticker} not found.")

    def get_company_submissions(self, cik: str) -> dict:
         url=settings.SEC_SUBMISSIONS_URL.format(
             cik=cik
         )

         response= requests.get(
             url,
             headers=self.headers,
             timeout=30
         )
         response.raise_for_status()
         return response.json()


    def get_latest_filing(
            self,
            cik: str,
            form_type: str
    ):

        submissions = self.get_company_submissions(cik)
        recent= submissions["filings"]["recent"]
        forms =recent["form"]

        for index, form in enumerate(forms):

            if form == form_type:
                return {
                    "form": form,
                    "filingDate": recent["filingDate"][index],
                    "accessionNumber": recent["accessionNumber"][index],
                    "primaryDocument": recent["primaryDocument"][index]
                }
        raise ValueError(
            f"No {form_type} filing found."
        )