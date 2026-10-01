"""Business services for greetings."""

from typing import Protocol

from app.domain import User


class GreetingServiceProtocol(Protocol):
    """Contract for producing a greeting for a user."""

    def create_greeting(self, user: User) -> str:
        """Return the greeting text for the supplied user."""


class GreetingService:
    """Creates the greeting required by the application contract."""

    def create_greeting(self, user: User) -> str:
        """Return a greeting containing the user's name."""
        return f"Hello {user.name}"
