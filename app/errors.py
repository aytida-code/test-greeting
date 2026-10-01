"""Centralized application error response support."""

import logging
from datetime import UTC, datetime
from uuid import uuid4

logger = logging.getLogger(__name__)


from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

ERROR_CODE_VALIDATION = "validation_error"
ERROR_CODE_INTERNAL = "internal_error"
GENERIC_ERROR_MESSAGE = "An unexpected error occurred."
VALIDATION_ERROR_MESSAGE = "The request is invalid."


def request_correlation_id(request: Request) -> str:
    """Return the caller's correlation ID or create a new one."""
    return getattr(request.state, "correlation_id", str(uuid4()))


def error_body(code: str, message: str, correlation_id: str) -> dict[str, str]:
    """Build the consistent, client-safe error envelope."""
    return {
        "code": code,
        "message": message,
        "timestamp": datetime.now(UTC).isoformat(),
        "correlation_id": correlation_id,
    }


def register_exception_handlers(app: FastAPI) -> None:
    """Register the application's centralized exception translations."""

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        del exc
        correlation_id = request_correlation_id(request)
        return JSONResponse(
            status_code=422,
            content=error_body(
                ERROR_CODE_VALIDATION, VALIDATION_ERROR_MESSAGE, correlation_id
            ),
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        correlation_id = request_correlation_id(request)
        logger.exception(
            "Unhandled request failure [correlation_id=%s]", correlation_id, exc_info=exc
        )
        return JSONResponse(
            status_code=500,
            content=error_body(ERROR_CODE_INTERNAL, GENERIC_ERROR_MESSAGE, correlation_id),
        )
