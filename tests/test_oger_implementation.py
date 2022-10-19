"""OGERImplementation test."""
import unittest

from oaklib.selector import get_implementation_from_shorthand

from tests import MORPHOLOGY, SHAPE


class TestOGERImplementation(unittest.TestCase):
    """OGERImplementation test."""

    def setUp(self) -> None:
        """Set up implementation."""
        self.oi = get_implementation_from_shorthand("oger:sqlite:obo:pato")

    def test_entities(self):
        """Test basic functionality."""
        curies = list(self.oi.entities())
        self.assertIn(SHAPE, curies)
        self.assertIn(MORPHOLOGY, curies)
