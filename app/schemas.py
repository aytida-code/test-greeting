"""API request and response schemas."""

from pydantic import BaseModel


class UserCreate(BaseModel):
    """The user name submitted to the greeting endpoint."""

    name: str


class GreetingResponse(BaseModel):
    """The greeting returned for a submitted user."""

    message: str
