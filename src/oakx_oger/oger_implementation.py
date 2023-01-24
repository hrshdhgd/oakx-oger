"""OGER Implementation."""
import csv
import logging
from dataclasses import dataclass
from io import TextIOWrapper
from multiprocessing import cpu_count
from pathlib import Path
from typing import Iterable, List

import pystow
import yaml
from nltk import ne_chunk, pos_tag, word_tokenize
from oaklib.datamodels.text_annotator import (
    TextAnnotation,
    TextAnnotationConfiguration,
)
from oaklib.interfaces import TextAnnotatorInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.selector import get_implementation_from_shorthand
from oger.ctrl.run import run as og_run

__all__ = [
    "OGERImplementation",
]

OX_OGER_MODULE = pystow.module("oxoger")
TERMS_DIR = OX_OGER_MODULE.join("terms")
OUT_DIR = OX_OGER_MODULE.join("output")
BIOLINK_CLASS = "biolink:OntologyClass"

# ! CLI command:
#   runoak
#   -i oger:sqlite:obo:bero
#   annotate
#   --text-file src/oakx_oger/input/nlpProposals.tsv
#   -x exclude.txt

OGER_CONFIG = {
    "include_header": "True",
    "pointer-type": "glob",
    "pointers": "*.txt",
    "iter-mode": "collection",
    "article-format": "txt",
    "export_format": "tsv",
    # "termlist1_path": "data/terms/pato_termlist.tsv",
    # "termlist_stopwords": "data/stopwords/stopWords.txt",
    "termlist_normalize": "lowercase stem-Porter",
    "postfilter": "builtin:remove_overlaps \
        builtin:remove_sametype_overlaps \
        builtin:remove_submatches  \
        builtin:remove_sametype_submatches",
}


@dataclass
class OGERImplementation(TextAnnotatorInterface, OboGraphInterface):
    """OGER Implementation."""

    terms_dir = TERMS_DIR
    output_dir = OUT_DIR
    input_dir = Path(__file__).resolve().parent / "input"
    stopwords_dir = Path(__file__).resolve().parent / "stopwords"

    def __post_init__(self):
        """Initialize the OGERImplementation class."""
        slug = self.resource.slug
        self.oi = get_implementation_from_shorthand(slug)
        ont = slug.split(":")[-1]
        self.termlist_fn = ont + "_termlist.tsv"
        self.termlist_pickle_fn = self.termlist_fn + ".pickle"
        self.stopwords = self.stopwords_dir / "stopwords.txt"
        self.ner_metadata = self.output_dir / "ner_metadata.yaml"
        self.outfile = "None.tsv"
        self.workers = cpu_count() // 2 - 1

    def _create_termlist(
        self, slug: str, path: Path, terms_to_remove: List[str]
    ) -> None:
        """
        Create an ontology termlist file which forms the ER dictionary.

        Format produced by the Bio Term Hub (UMLS CUI first).

        [0] UMLS CUI, [1] resource from which it comes,
        [2] native ID, [3] term, [4] preferred form, [5] type
        """
        with open(path, "w") as t:
            for node in self.oi.entities():
                if self.oi.label(node) and self.oi.label(
                    node
                ).casefold() not in map(
                    lambda tok: tok.casefold(), terms_to_remove
                ):
                    t.write(
                        "\t".join(
                            [
                                "CUI-less",
                                slug,
                                node,
                                self.oi.label(node),
                                self.oi.label(node),
                                BIOLINK_CLASS,
                            ]
                        )
                        + "\n"
                    )

    def annotate_file(
        self,
        text_file: Path,
        configuration: TextAnnotationConfiguration,
    ) -> Iterable[TextAnnotation]:
        """Annotate text from a file.

        :param text: Text to be annotated.
        :param configuration: TextAnnotationConfiguration , defaults to None
        :yield: Annotated result
        """
        termlist_filepath = self.terms_dir / self.termlist_fn
        termlist_pickle_filepath = self.terms_dir / self.termlist_pickle_fn
        with open(self.stopwords, "r") as st:
            stopwords = set(st.read().splitlines())
        if hasattr(configuration, "token_exclusion_list"):
            configuration.token_exclusion_list.extend(list(stopwords))
        else:
            configuration.token_exclusion_list = list(stopwords)

        if termlist_pickle_filepath.is_file():
            logging.info(f"Termlist exists at {termlist_pickle_filepath}")
        elif termlist_filepath.is_file():
            logging.info(f"Termlist exists at {termlist_filepath}")
        else:
            self._create_termlist(
                self.resource.slug,
                termlist_filepath,
                configuration.token_exclusion_list,
            )

        if isinstance(text_file, TextIOWrapper):
            text_file = Path(text_file.name)
            self.outfile = text_file.name
            if text_file.suffix == ".tsv":
                OGER_CONFIG["pointers"] = "*" + text_file.suffix
                OGER_CONFIG["article-format"] += "_tsv"
        OGER_CONFIG["input-directory"] = str(text_file.resolve().parent)
        OGER_CONFIG["output-directory"] = str(self.output_dir)
        OGER_CONFIG["termlist_path"] = str(termlist_filepath)
        OGER_CONFIG["termlist_stopwords"] = str(self.stopwords)

        og_run(n_workers=self.workers, **OGER_CONFIG)
        self.post_output = self.output_dir / self.outfile.replace(
            ".tsv", "_postProcessed.tsv"
        )
        with open(text_file, "r") as f:
            text_list = f.readlines()
            tagged_dict: dict = {}
            for i, text in enumerate(text_list):
                if "\t" in text:
                    idx, txt = text.strip().split("\t")
                else:
                    idx = str(i)
                    txt = text.strip()
                if txt != "text":
                    if idx not in tagged_dict:
                        tagged_dict[idx] = {}
                    for named_entity in ne_chunk(
                        pos_tag(list(set(word_tokenize(txt))))
                    ):
                        if isinstance(named_entity, tuple):
                            token, pos = named_entity
                            tagged_dict[idx][token] = {
                                "POS": pos,
                            }

                        else:
                            token, pos = named_entity[0]
                            tagged_dict[idx][token] = {
                                "POS": pos,
                                "entity": named_entity.label(),
                            }

            with open(self.ner_metadata, "w") as f:
                yaml.safe_dump(tagged_dict, f)

        with open(self.output_dir / self.outfile, "r") as f, open(
            self.post_output, "w", newline=""
        ) as o:
            input_reader = csv.DictReader(f, delimiter="\t")
            for row in input_reader:
                if "fieldnames" not in locals():
                    fieldnames = list(row.keys())
                    fieldnames.extend(["POS", "entity"])
                    output_writer = csv.DictWriter(
                        o, delimiter="\t", fieldnames=fieldnames
                    )
                    output_writer.writeheader()
                if row["DOCUMENT ID"] in tagged_dict:
                    # Usual TSV inpput file
                    if row["MATCHED TERM"] in tagged_dict[row["DOCUMENT ID"]]:
                        row.update(
                            tagged_dict[row["DOCUMENT ID"]][
                                row["MATCHED TERM"]
                            ]
                        )
                    elif (
                        row["MATCHED TERM"].lower()
                        in tagged_dict[row["DOCUMENT ID"]]
                    ):
                        row.update(
                            tagged_dict[row["DOCUMENT ID"]][
                                row["MATCHED TERM"].lower()
                            ]
                        )
                    else:
                        logging.info(
                            f"{row['MATCHED TERM']} doesn't have \
                                POS/entity info."
                        )
                else:
                    # Text is provided or txt file used.
                    for _, v in tagged_dict.items():
                        if row["MATCHED TERM"] in v:
                            row.update(v[row["MATCHED TERM"]])
                        elif row["MATCHED TERM"].lower() in v:
                            row.update(v[row["MATCHED TERM"].lower()])
                        else:
                            logging.info(
                                f"{row['MATCHED TERM']} doesn't have \
                                    POS/entity info."
                            )

                output_writer.writerow(row)

                yield TextAnnotation(
                    object_id=row["ENTITY ID"],
                    object_label=row["MATCHED TERM"],
                    subject_start=row["START POSITION"],
                    subject_end=row["END POSITION"],
                    subject_text_id=row["DOCUMENT ID"],
                )

    def annotate_text(
        self, text: str, configuration: TextAnnotationConfiguration
    ) -> Iterable[TextAnnotation]:
        """Annotate text from a file.

        :param text: Text to be annotated.
        :param configuration: TextAnnotationConfiguration , defaults to None
        :yield: Annotated result
        """
        text_file: Path = self.input_dir / "tmp/input.txt"
        text_file.parent.mkdir(exist_ok=True, parents=True)
        text_file.write_text(text)
        yield from self.annotate_file(text_file, configuration)
