"""OGERImplementation test."""
import unittest
from pathlib import Path

import pandas as pd
from oaklib.datamodels.text_annotator import TextAnnotationConfiguration
from oaklib.selector import get_implementation_from_shorthand

from oakx_oger.synonymizer.synonymize import (
    create_new_rows_based_on_rules,
    get_rules_table_from_file,
)
from tests import ORGANISMS, RULES_FILE

TEST_DIR = Path(__file__).resolve().parent


class TestOGERImplementation(unittest.TestCase):
    """OGERImplementation test."""

    def setUp(self) -> None:
        """Set up implementation."""
        self.impl = get_implementation_from_shorthand("oger:sqlite:obo:pato")
        self.input_file = TEST_DIR / "input/text.txt"
        self.impl.output_dir = TEST_DIR / "output/"
        self.impl.terms_dir = TEST_DIR / "terms/"
        self.input_words = (
            "cultured organisms polar ecosystems atmospheric gas exchange"
        )
        self.configuration = TextAnnotationConfiguration()
        self.rules_df = get_rules_table_from_file(RULES_FILE)
        self.termlist = TEST_DIR / "input/syn/termlist.tsv"

    def test_annotate_file(self):
        """Test annotation of a file."""
        results = list(
            self.impl.annotate_file(self.input_file, self.configuration)
        )
        self.assertEqual(len(results), 13)
        self.assertTrue(ORGANISMS in [x.object_id for x in results])

    def test_annotate_text(self):
        """Test annotation of text."""
        results = list(
            self.impl.annotate_text(self.input_words, self.configuration)
        )
        self.assertEqual(len(results), 3)
        self.assertTrue(ORGANISMS in [x.object_id for x in results])

    def test_rules_file_parse(self):
        """Test synonymizer rules."""
        self.assertTrue(isinstance(self.rules_df, pd.DataFrame))

    def test_synonymizer_tests(self):
        """Test tests in rules file."""
        new_synonymized_rows = create_new_rows_based_on_rules(
            self.rules_df, self.termlist
        )
        self.assertTrue(len(new_synonymized_rows), 32)
