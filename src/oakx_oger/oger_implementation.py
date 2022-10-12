"""OGER Implementation."""
from dataclasses import dataclass

from oaklib.interfaces import TextAnnotatorInterface


@dataclass
class OGERImplementation(TextAnnotatorInterface):
    """OGER Implementation."""

    def __post_init__(self):
        """Initialize the OGERImplementation class."""
        pass
