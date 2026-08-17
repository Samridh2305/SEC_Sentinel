import logging
import os

import requests
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from openai import OpenAIError
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.cors import CORSMiddleware

from api.answer_api import router as answer_router
from api.compare_api import router as comparison_router
from api.ask_api import router as ask_router
from api.data_api import router as data_router
from api.company_api import router as company_router


app = FastAPI(
    title="SEC Sentinel"
)

app.include_router(
    answer_router
)

app.include_router(
    comparison_router
)

app.include_router(
    ask_router
)

app.include_router(
    data_router
)

app.include_router(
    company_router
)
@app.get("/")
def root():

    return {
        "message": "SEC Sentinel API is running"
    }