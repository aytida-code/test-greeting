"""Domain entities for the greeting feature."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class User:
    """A user represented solely by the supplied name."""

    name: str
