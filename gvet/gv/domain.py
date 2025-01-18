"""domain model implementation"""

from dataclasses import asdict, dataclass, field
from typing import Optional


@dataclass
class Term:
    """A term associated with a Subject

    Attributes:
        label: the term's text
        language: the term's language
        type: either gvp_preferred, preferred, or alternative
        part_of_speach: Noun, Verb for example
    """

    label: str
    language: str
    type: str
    part_of_speech: Optional[str] = ""


@dataclass
class Note:
    text: str
    language: str


@dataclass
class SubjectInfo:
    """
    Just the basic info about a subject.

    Attributes:
        id: the unique identifier, ex. aat:300263388
        name: the gv-preferred term
        record_type: facet, hierarchy, guide, concept
        note: (optional) the english language scopeNote

    """

    id: str
    name: str
    record_type: str

    def as_subject(self) -> "Subject":
        """Return a Subject instance"""
        data = asdict(self)
        return Subject(**data)


@dataclass
class Subject:
    id: str
    name: str
    record_type: str
    notes: list[Note] = field(default_factory=list)
    terms: list[Term] = field(default_factory=list)
    ancestors: list[SubjectInfo] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            name=data["name"],
            record_type=data["record_type"],
            notes=[Note(**n_data) for n_data in data.get("notes", [])],
            terms=[Term(**t_data) for t_data in data.get("terms", [])],
            ancestors=[SubjectInfo(**a_data) for a_data in data.get("ancestors", [])],
        )

    def as_dict(self) -> dict:
        return asdict(self)


def make_id(data: dict[str, str]) -> str:
    return f"{data['scheme_prefix']}:{data['identifier']}"
