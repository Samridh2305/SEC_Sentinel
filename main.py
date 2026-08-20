from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from api.answer_api import router as answer_router
from api.ask_api import router as ask_router
from api.company_api import router as company_router
from api.compare_api import router as comparison_router
from api.filing_router import router as filing_router
from api.sec_router import router as sec_router
from common.logger import logger
from exceptions.custom_exceptions import AppException, BadRequestException
from exceptions.exception_handler import app_exception_handler

app = FastAPI(
    title="SEC Sentinel"
)

app.add_exception_handler(AppException, app_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
):
    return await app_exception_handler(
        request,
        BadRequestException("The request data is invalid."),
    )


@app.exception_handler(Exception)
async def unexpected_exception_handler(request: Request, exc: Exception):
    logger.exception("Unexpected application failure")
    return JSONResponse(
        status_code=500,
        content={"detail": AppException.detail},
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
    sec_router
)

app.include_router(
    company_router
)
app.include_router(
    filing_router
)


@app.get("/")
def root():
    return {
        "message": "SEC Sentinel API is running"
    }
