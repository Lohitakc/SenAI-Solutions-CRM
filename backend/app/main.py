import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app.api.email_routes import router as email_router
from app.core.exception_handlers import (
    app_error_handler,
    database_error_handler,
    unexpected_error_handler,
    validation_error_handler,
)
from app.services.exceptions import AppError


logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logging.getLogger(__name__).info("Application startup complete.")
    yield
    logging.getLogger(__name__).info("Application shutdown complete.")


app = FastAPI(
    title="SenAI Solutions CRM API",
    version="0.1.0",
    description="Backend foundation for the SenAI Solutions CRM platform.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(SQLAlchemyError, database_error_handler)
app.add_exception_handler(Exception, unexpected_error_handler)

app.include_router(email_router, prefix="/api", tags=["Email Ingestion"])

@app.get("/health", tags=["System"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
