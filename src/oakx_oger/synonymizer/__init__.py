"""Synonymizer module."""
from oakx_oger.synonymizer.synonymize import (
    create_new_rows_based_on_rules,
    get_rules_table,
    get_rules_table_from_file,
)

__all__ = [
    "get_rules_table",
    "get_rules_table_from_file",
    "create_new_rows_based_on_rules",
]
