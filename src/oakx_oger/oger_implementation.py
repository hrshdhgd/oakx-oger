"""OGER Implementation."""
from dataclasses import dataclass
import logging
from typing import Iterable, Iterator

import pandas as pd
from oaklib.datamodels.text_annotator import (
    TextAnnotation,
    TextAnnotationConfiguration,
)
from oaklib.interfaces import TextAnnotatorInterface
from oaklib.interfaces.obograph_interface import OboGraphInterface
from oaklib.selector import get_implementation_from_shorthand
from oaklib.utilities.rate_limiter import check_limit
from pathlib import Path
from oaklib.types import CURIE
# from oger.er.entity_recognition import EntityRecognizer
TERMS_DIR = Path(__file__).resolve().parent / "terms"

@dataclass
class OGERImplementation(TextAnnotatorInterface, OboGraphInterface):
    """OGER Implementation."""

    # oger_client_class: ClassVar[type[EntityRecognizer]]

    def __post_init__(self):
        """Initialize the OGERImplementation class."""
        slug = self.resource.slug
        self.oi = get_implementation_from_shorthand(slug)

        # node_columns = ["subject_id", "subject_label"]
        # node_table = pd.DataFrame(columns=node_columns)
        # edges_columns = ["subject_id", "predicate_id", "object_id"]
        # edges_table = pd.DataFrame(columns=edges_columns)
        # for rel in oi.all_relationships():
        #     edges_table = pd.concat([edges_table,pd.DataFrame([rel], columns=edges_columns)], ignore_index=True)
        ont = slug.split(":")[-1]
        termlist_fn = ont+"_termlist.tsv"
        termlist_filepath = TERMS_DIR / termlist_fn
        if termlist_filepath.is_file():
            # termlist_df = pd.read_csv(termlist_file, sep='\t',low_memory=False)
            logging.info(
                    f"Termlist exists at {termlist_filepath}"
                )
        else:
            self._create_termlist(slug, termlist_filepath)
        
                
    def _create_termlist(self, slug:str, path:Path) -> None:
        """Create an ontology termlist file which forms the ER dictionary. """
        with open(path, 'w') as t:
            for node in self.oi.entities():
                if self.oi.label(node):
                    t.write("\t".join(["CUI-less", slug, node, self.oi.label(node), self.oi.label(node)])+"\n")

    def entities(self, filter_obsoletes=True, owl_type=None) -> Iterable[CURIE]:
        """Implement OAK interface."""
        for n_id in self.oi.entities():
            yield n_id

    def _get_response(self, *args, **kwargs):
        check_limit()
        # self.client.recognize_entities("cell")
        # return self.client.get_response(*args, **kwargs)

    def _get_json(self, *args, **kwargs):
        # response = self._get_response(*args, **kwargs)
        # return response.json()
        pass

    def annotate_text(
        self, text: str, configuration: TextAnnotationConfiguration = None
    ) -> Iterator[TextAnnotation]:
        """Annotate text.

        :param text: Text to be annotated.
        :param configuration: _description_, defaults to None
        :return: _description_
        :yield: _description_
        """
        # COPIED FROM ontoportal_implementation in oaklib

        # if configuration is None:
        #     configuration = TextAnnotationConfiguration()
        # logging.info(f"Annotating text: {text}")
        # # include =['prefLabel', 'synonym', 'definition',\
        #           'semanticType', 'cui']
        # include = ["prefLabel", "semanticType", "cui"]
        # require_exact_match = True
        # include_str = ",".join(include)
        # params = {
        #           "include": include_str,
        #           "require_exact_match": require_exact_match,
        #           "text": text
        #           }
        # if self.resource and self.resource.slug:
        #     params["ontologies"] = self.resource.slug.upper()
        # results = self._get_json("/annotator", params=params)
        # return self._annotator_json_to_results(results, text, configuration)
        pass
