import logging
from typing import Any

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.services.exceptions import AppError

logger = logging.getLogger(__name__)


def error_response(status_code: int, error_code: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": error_code,
                "message": message,
            }
        },
    )


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    logger.warning("Application error on %s: %s", request.url.path, exc.message)
    return error_response(exc.status_code, exc.error_code, exc.message)


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.warning("Validation error on %s: %s", request.url.path, exc.errors())
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "validation_error",
                "message": "Request validation failed.",
                "details": _json_safe_errors(exc.errors()),
            }
        },
    )


def _json_safe_errors(errors: list[dict[str, Any]]) -> list[dict[str, Any]]:
    safe_errors: list[dict[str, Any]] = []
    for error in errors:
        safe_error = dict(error)
        if "ctx" in safe_error:
            safe_error["ctx"] = {key: str(value) for key, value in safe_error["ctx"].items()}
        safe_errors.append(safe_error)
    return safe_errors


async def database_error_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    logger.error("Database error on %s", request.url.path)
    return error_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "database_error",
        "A database error occurred.",
    )


async def unexpected_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Unexpected error on %s", request.url.path)
    return error_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "internal_error",
        "An unexpected error occurred.",
    )
