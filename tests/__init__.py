"""Tests for oakx-oger."""

from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
SYNONYMER_DIR = PROJECT_DIR.joinpath("src/oakx_oger/synonymizer/")
RULES_FILE = SYNONYMER_DIR.joinpath("synonym_rules.yaml")

TESTS_DIR = Path(__file__).resolve().parent
INPUT_DIR = Path(TESTS_DIR) / "input"
OUTPUT_DIR = Path(TESTS_DIR) / "output"
TEST_OWL = INPUT_DIR / "go-nucleus.owl"

CHEBI_NUCLEUS = "CHEBI:33252"
NUCLEUS = "GO:0005634"
NUCLEAR_ENVELOPE = "GO:0005635"
THYLAKOID = "GO:0009579"

SHAPE = "PATO:0000052"
MORPHOLOGY = "PATO:0000051"
ORGANISMS = "UBERON:0000062"


def output_path(fn: str) -> str:
    """Return the path to the output file."""
    return str(Path(OUTPUT_DIR) / fn)
