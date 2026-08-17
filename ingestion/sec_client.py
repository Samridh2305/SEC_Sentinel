import requests

from common.config import settings
from common.logger import logger
from exceptions.custom_exceptions import NotFoundException, ServiceException


class SECClient:

    def __init__(self):
        self.headers = {
            "User-Agent": "Samridh samridh2305@gmail.com"
        }
        self.companies: dict | None = None

    def _get_companies(self) -> dict:
        if self.companies is None:
            self.companies = self._load_companies()
        return self.companies

    def _load_companies(self) -> dict:
        return self._get_json(settings.SEC_COMPANY_TICKERS_URL)

    def _get_json(self, url: str) -> dict:
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError) as exc:
            logger.exception("SEC request failed for %s", url)
            raise ServiceException() from exc

    def get_company_cik(
            self,
            ticker: str
    ) -> str:

        ticker = ticker.upper()

        for company in self._get_companies().values():

            if company["ticker"] == ticker:
                cik = str(company["cik_str"])

                return cik.zfill(10)

        raise NotFoundException(
            f"Ticker {ticker} not found."
        )

    def search_company(
        self,
        company_name: str
    ) -> list[dict]:

        search_term = company_name.lower()

        results = []

        for company in self._get_companies().values():

            title = company["title"]

            if search_term in title.lower():

                results.append({
                    "company": title,
                    "ticker": company["ticker"],
                    "cik": str(
                        company["cik_str"]
                    ).zfill(10)
                })

        return results

    def get_company_submissions(
        self,
        cik: str
    ) -> dict:

        url = settings.SEC_SUBMISSIONS_URL.format(
            cik=cik
        )

        return self._get_json(url)


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
        raise NotFoundException(
            f"No {form_type} filing found."
        )

    def get_filing(
            self,
            cik: str,
            form_type: str,
            filing_date: str
    ):
        submissions = self.get_company_submissions(cik)

        recent = submissions["filings"]["recent"]

        for index, form in enumerate(recent["form"]):

            if (
                    form == form_type
                    and recent["filingDate"][index] == filing_date
            ):
                return {
                    "form": form,
                    "filingDate": recent["filingDate"][index],
                    "accessionNumber": recent["accessionNumber"][index],
                    "primaryDocument": recent["primaryDocument"][index]
                }

        raise NotFoundException(
            f"No {form_type} filing found for {filing_date}."
        )

    def get_all_filings(
            self,
            ticker: str,
            form_type: str
    ) -> list[dict]:

        cik = self.get_company_cik(
            ticker
        )

        submissions = self.get_company_submissions(
            cik
        )

        recent = submissions["filings"]["recent"]

        results = []

        for index, form in enumerate(
                recent["form"]
        ):

            if form == form_type:
                results.append({
                    "form_type": form,
                    "filing_date": recent["filingDate"][index],
                    "accession_number": recent["accessionNumber"][index],
                    "primary_document": recent["primaryDocument"][index]
                })

        if not results:
            raise NotFoundException(
                f"No {form_type} filings found for {ticker}."
            )

        return results
