"""FastAPI entry point for the greeting API."""

import logging
from collections.abc import Awaitable, Callable
from uuid import uuid4

from fastapi import Depends, FastAPI, Request
from starlette.responses import Response

from app.domain import User
from app.errors import register_exception_handlers
from app.schemas import GreetingResponse, UserCreate
from app.services import GreetingService, GreetingServiceProtocol

logger = logging.getLogger(__name__)
HEALTH_STATUS = "ok"

app = FastAPI(title="Greeting API", version="1.0.0")


@app.middleware("http")
async def add_correlation_id(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """Attach a request correlation ID to the response and request context."""
    correlation_id = (
        request.headers.get("X-Request-ID")
        or request.headers.get("X-Correlation-ID")
        or str(uuid4())
    )
    request.state.correlation_id = correlation_id
    response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id
    return response


def get_greeting_service() -> GreetingServiceProtocol:
    """Provide the greeting service dependency for route handlers."""
    return GreetingService()


@app.get("/health")
def health() -> dict[str, str]:
    """Return the unauthenticated operational health status."""
    return {"status": HEALTH_STATUS}


@app.post("/greet", response_model=GreetingResponse)
def greet(
    user_create: UserCreate,
    request: Request,
    greeting_service: GreetingServiceProtocol = Depends(get_greeting_service),
) -> GreetingResponse:
    """Return the required greeting for the submitted user name."""
    user = User(name=user_create.name)
    message = greeting_service.create_greeting(user)
    logger.info(
        "Greeting created [correlation_id=%s, name_length=%s]",
        request.state.correlation_id,
        len(user.name),
    )
    return GreetingResponse(message=message)


register_exception_handlers(app)
