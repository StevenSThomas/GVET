"""This module provides functionality to execute queries against a the Getty Vocabularies SPARQL endpoint


Classes:
    QueryService: a service class to prepare and execute queries
    QueryResult: container for results

Usage:
    qs = QueryService()
    result = qs.execute_named_query("get_subject_by_id",id="aat:30022688")

"""

import time
from dataclasses import dataclass
from logging import getLogger
from pathlib import Path
from string import Template
from typing import Optional

import httpx

from gvet.gv.exceptions import ObjectDoesNotExist

__all__ = ("QueryService", "QueryResult")

_logger = getLogger(__name__)


class QueryTemplate(Template):
    """
    Template Class for sparql queries to allow parameters to be passed into a query

    Uses @ as a delimiter because braces are heavily used in sparql

    """

    delimiter = "@"


@dataclass(frozen=True)
class QueryResult:
    """
    Container for query results

    Attributes:
        query_text: the sparql query text that produced this result
        execution_time_seconds: number of seconds it took to return the results
        cols: list of column names
        rows: the rows of data returned as Dict objects
    """

    query_text: str
    execution_time_seconds: float
    cols: list[str]
    rows: list[dict[str, str]]

    def first(self) -> dict[str, str]:
        """
        Return the first row returned from the query. None if no rows returned.

        Raises:
            ObjectDoesNotExist - if no rows are returned
        """

        if self.rows:
            return self.rows[0]
        raise ObjectDoesNotExist()


class QueryService:
    """Service for querying the Getty Vocabularies sparql endpoint"""

    ENDPOINT = "https://vocab.getty.edu/sparql.json"

    def __init__(self, template_folder: Optional[Path] = None):
        """Create a new service instance

        Args:
            template_folder: (optional) the folder where sparql query files are located
                defaults to the 'queries' folder.
        """
        self.template_folder = (
            template_folder or Path(__file__).parent.resolve() / "query_templates"
        )
        self.templates: dict[str : QueryService.QueryTemplate] = {}
        self.load_templates()

    def __repr__(self):
        return f"QueryService({self.ENDPOINT},{self.template_folder})"

    def load_templates(self):
        """Load/reload templates from the file system. Templates are automatically loaded when the service is created"""
        self.templates = {}
        pathlist = self.template_folder.glob("*.sparql")
        for path in pathlist:
            with open(path, "r") as template_file:
                template_text = template_file.read()
            self.set_template(path.stem, template_text)

    def set_template(self, name: str, template_text: str):
        """Set a template by name and the template text.  Mostly used for testing."""
        self.templates[name] = QueryTemplate(template_text)

    def prepare_named_query(self, template_name: str, **params) -> str:
        try:
            query_template = self.templates[template_name]
        except KeyError:
            _logger.error(
                "query templated named ${template_name}s not found.",
                {"template_name": template_name},
            )
            raise ValueError(f"Template named {template_name} not found.")
        query = query_template.substitute(**params)
        return query

    def execute_query(self, query: str) -> QueryResult:
        """Executes a sparql query

        Args:
          query: the prepared spa
        """
        _logger.debug("executing query ```%(query)s```", {"query": query})

        query_start_time = time.time()
        response = httpx.get(url=self.ENDPOINT, params={"query": query})
        response.raise_for_status()
        raw_response = response.json()

        return QueryResult(
            query_text=query,
            execution_time_seconds=time.time() - query_start_time,
            cols=raw_response["head"]["vars"],
            rows=[
                clean_row_data(row_data)
                for row_data in raw_response["results"]["bindings"]
            ],
        )

    def execute_named_query(self, query_name: str, **params) -> QueryResult:
        query = self.prepare_named_query(query_name, **params)
        return self.execute_query(query)


def clean_row_data(row_data: dict[str, dict]) -> dict[str, str]:
    return {key: data["value"] for key, data in row_data.items()}
