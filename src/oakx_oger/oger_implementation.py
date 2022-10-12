"""OGER Implementation."""
from dataclasses import dataclass

from oaklib.interfaces import BasicOntologyInterface


@dataclass
class OGERImplementation(BasicOntologyInterface):
    """OGER Implementation."""

    def __post_init__(self):
        """Initialize the OGERImplementation class."""
        pass
