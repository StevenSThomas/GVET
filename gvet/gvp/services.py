import httpx
from typing import Protocol
from abc import abstractmethod
from .dataclasses import Subject, SubjectType


class Transport(Protocol):
    @abstractmethod
    def execute_query(self, query: str) -> dict:
        raise NotImplementedError


class HttpTransport(Transport):
    def __init__(self, endpoint: str = None):
        self.endpoint = endpoint or "https://vocab.getty.edu/sparql.json"

    def execute_query(self, query: str, implicit: bool = True) -> dict:
        response = httpx.get(url=self.endpoint, params={"query": query})
        response.raise_for_status()
        result = response.json()
        return result["results"]["bindings"]

    def __repr__(self):
        return f"HttpTransport({self.endpoint})"


class QueryService:
    def __init__(self, transport: Transport = None):
        self._transport = transport or HttpTransport()

    def __repr__(self):
        return f"QueryService({self._transport})"

    def _execute_query(self, query: str) -> dict:
        return self._transport.execute_query(query=query)

    def get_facets(self) -> list[Subject]:
        """
        Returns the top most subjects in the AAT scheme
        """
        query = """
         select ?id ?label ?note ?type ?parent_string WHERE {  
            ?subject a gvp:Facet;
                skos:inScheme aat:;
                dc:identifier ?id;
                gvp:prefLabelGVP/xl:literalForm ?label;
                skos:scopeNote [dct:language gvp_lang:en; rdf:value ?note];
                gvp:parentString ?parent_string;
                a ?typ.
            ?typ rdfs:subClassOf gvp:Subject; rdfs:label ?type.
          filter (?typ != gvp:Subject)
        }
        """
        items = self._execute_query(query)
        return [parse_subject(item) for item in items]

    def get_subject_members(self, subject_id: int) -> list[Subject]:
        """
        Returns a list of Subjects in which each returned subjects broadPreferred matches the subject_id argument.
        """
        query_template = """
         select ?id ?label ?note ?type ?parent_string WHERE {{  
            ?subject gvp:broaderPreferred {subject_id};
                skos:inScheme aat:;
                dc:identifier ?id;
                gvp:prefLabelGVP/xl:literalForm ?label;
                skos:scopeNote [dct:language gvp_lang:en; rdf:value ?note];
                gvp:parentString ?parent_string;
                a ?typ.
            ?typ rdfs:subClassOf gvp:Subject; rdfs:label ?type.
          filter (?typ != gvp:Subject)
        }} 
        """
        query = query_template.format(subject_id=subject_id)
        items = self._execute_query(query)
        return [parse_subject(item) for item in items]


def parse_subject(item: dict) -> Subject:
    """Parses the dictionary returned for each subject in a query into a Subject dataclass."""
    return Subject(
        id=f"aat:{item["id"]["value"]}",
        label=item["label"]["value"],
        note=item["note"]["value"],
        type=SubjectType(item["type"]["value"]),
        parent_names=item["parent_string"]["value"].split(","),
    )
