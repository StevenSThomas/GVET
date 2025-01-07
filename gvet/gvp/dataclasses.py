from dataclasses import dataclass
from enum import StrEnum


class SubjectType(StrEnum):
    FACET = "Facet"
    HIERARCHY = "Hierarchy"
    GUIDE_TERM = "Guide Term"
    CONCEPT = "Concept"


@dataclass
class Subject:
    id: str
    type: SubjectType
    label: str
    note: str
    parent_names: list[str]
