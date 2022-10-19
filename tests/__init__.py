"""Tests for oakx-oger."""

import os
from pathlib import Path

ROOT = os.path.abspath(os.path.dirname(__file__))
INPUT_DIR = Path(ROOT) / "input"
OUTPUT_DIR = Path(ROOT) / "output"
TEST_OWL = INPUT_DIR / "go-nucleus.owl"

CHEBI_NUCLEUS = "CHEBI:33252"
NUCLEUS = "GO:0005634"
NUCLEAR_ENVELOPE = "GO:0005635"
THYLAKOID = "GO:0009579"

SHAPE = "PATO:0000052"
MORPHOLOGY = "PATO:0000051"


def output_path(fn: str) -> str:
    """Return the path to the output file."""
    return str(Path(OUTPUT_DIR) / fn)
