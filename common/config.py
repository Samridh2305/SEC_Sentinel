import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Project root (SEC_Sentinel/)
    PROJECT_ROOT = Path(__file__).resolve().parent.parent

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    CORS_ALLOW_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True

    # SEC API CONFIGURATIONS
    SEC_COMPANY_TICKERS_URL = os.getenv("SEC_COMPANY_TICKERS_URL")
    SEC_SUBMISSIONS_URL = os.getenv("SEC_SUBMISSIONS_URL")
    SEC_ARCHIVES_URL = os.getenv("SEC_ARCHIVES_URL")

    # Local storage
    RAW_FILINGS_DIR = PROJECT_ROOT / os.getenv(
        "RAW_FILINGS_DIR",
        "data/raw/filings"
    )


settings = Settings()