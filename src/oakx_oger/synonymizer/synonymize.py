"""Synonymizer module."""
from pathlib import Path

import pandas as pd
import yaml

RULES_DIR = Path(__file__).resolve().parent
RULES_FILE = RULES_DIR.joinpath("synonym_rules.yaml")
RELEVANT_COLUMNS = [
    "type",
    "match",
    "match_scope",
    "replacement",
    "qualifier",
    "ontology",
    "tests",
]


def get_rules_table_from_file(rules_file: Path = RULES_FILE):
    """Parse rules file to return table."""
    with open(rules_file, "r", encoding="utf-8") as f:
        rules = yaml.safe_load(f)

    list_of_rules = rules["rules"]
    return get_rules_table(list_of_rules)


def get_rules_table(list_of_rules: list) -> pd.DataFrame:
    """Return a dataframe of rules from YAML."""
    df = pd.DataFrame(list_of_rules)
    df["ontology"] = df["tests"].apply(lambda x: x[0]["ontology"])
    return df[RELEVANT_COLUMNS]


def create_new_rows_based_on_rules(
    rules_df: pd.DataFrame, termlist: Path
) -> pd.DataFrame:
    """Parse terms and rules to form additional rows of terms."""
    columns_of_interest_for_rules = [
        "type",
        "match",
        "match_scope",
        "replacement",
    ]
    terms_cols = [
        "cui",
        "source",
        "id",
        "match_term",
        "preferred_term",
        "category",
    ]
    terms_df = pd.read_csv(
        termlist, delimiter="\t", index_col=None, names=terms_cols
    )
    ontology_prefixes = rules_df["ontology"].drop_duplicates().values.tolist()

    new_terms_df = pd.DataFrame(columns=terms_cols)

    for ont in ontology_prefixes:
        rule_subset = rules_df.loc[rules_df["ontology"] == ont][
            columns_of_interest_for_rules
        ]
        terms_df_subset = terms_df.loc[
            terms_df["id"].str.startswith(ont, na=False)
        ]
        for rule_row in rule_subset.iterrows():
            need_syn_df = terms_df_subset[
                terms_df_subset["match_term"].str.match(
                    rule_row[1]["match"] + "$"
                )
            ]
            for syn_row in need_syn_df.iterrows():
                syn_row_df = (
                    syn_row[1]
                    .to_frame()
                    .T.reset_index()
                    .drop(["index"], axis=1)
                )

                term_to_replace = rule_row[1]["match"] + "$"
                replacement_term = rule_row[1]["replacement"]

                syn_row_df["match_term"] = syn_row_df["match_term"].replace(
                    term_to_replace,
                    replacement_term,
                    regex=True,
                )

                new_terms_df = pd.concat([new_terms_df, syn_row_df])
    return new_terms_df


def main():
    """Pass."""
    pass


if __name__ == "__main__":
    main()
