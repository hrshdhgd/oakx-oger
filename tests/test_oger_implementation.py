"""OGERImplementation test."""
import unittest
from pathlib import Path

from oaklib.datamodels.text_annotator import TextAnnotationConfiguration
from oaklib.selector import get_implementation_from_shorthand

from tests import ORGANISMS


class TestOGERImplementation(unittest.TestCase):
    """OGERImplementation test."""

    def setUp(self) -> None:
        """Set up implementation."""
        self.impl = get_implementation_from_shorthand("oger:sqlite:obo:pato")
        self.input_file = Path(__file__).resolve().parent / "input/text.txt"
        self.input_words = (
            "cultured organisms polar ecosystems atmospheric gas exchange"
        )
        self.configuration = TextAnnotationConfiguration()

    def test_annotate_file(self):
        """Test annotation of a file."""
        results = list(
            self.impl.annotate_file(self.input_file, self.configuration)
        )
        self.assertEqual(len(results), 13)
        self.assertTrue(ORGANISMS in [x.subject_text_id for x in results])

    def test_annotate_text(self):
        """Test annotation of text."""
        results = list(
            self.impl.annotate_text(self.input_words, self.configuration)
        )
        self.assertEqual(len(results), 3)
        self.assertTrue(ORGANISMS in [x.subject_text_id for x in results])
