"""Getty Vocabulary dataclasses to define the shape of the data returned"""

from typing import Optional

from gvet.gv import search_utils

from .domain import Note, Subject, SubjectInfo, Term, make_id
from .queries import QueryService

__all__ = [
    "Vocabulary",
]


class Vocabulary:
    """API for interacting with the Getty Vocabularies"""

    def __init__(
        self, query_service: Optional[QueryService] = None, cache_service=None
    ):
        """"""
        self._qs = query_service or QueryService()
        self._cache = cache_service

    def set_cache_service(self, cache_service):
        self._cache = cache_service

    def get_subject_info(self, id: str) -> SubjectInfo:
        """
        Return the basic subject info for a subject based on the id.

        Raises:
            ObjectDoesNotExist - if no subject exists with the provided id.
        """
        data = self._qs.execute_named_query("get_subject_by_id", id=id).first()
        return SubjectInfo(
            id=make_id(data),
            name=data["name"],
            record_type=data["record_type"],
        )

    def get_subject_detail(self, id: str) -> Subject:
        """
        Get a subject instance by its id.

        Args:
            id: the id of the subject to find. example: aat:300254607"

        Returns:
            a subject instance
        """
        if self._cache:
            subject = self._cache.get_subject(id=id)
            if subject:
                return subject

        subject_info = self.get_subject_info(id=id)
        subject = subject_info.as_subject()
        subject.notes = self.get_notes(id)
        subject.ancestors = self.get_ancestors(id)
        subject.terms = self.get_terms(id)

        if self._cache:
            self._cache.set_subject(subject)
        return subject

    def get_terms(self, subject_id: str) -> list[Term]:
        """Gets a list of terms for a subject in display order."""
        query_results = self._qs.execute_named_query("get_terms", subject_id=subject_id)
        return [Term(**row) for row in query_results.rows]

    def get_notes(self, subject_id: str) -> list[Note]:
        """Gets the list of scope notes for a subject in display order"""
        query_results = self._qs.execute_named_query("get_notes", subject_id=subject_id)
        return [Note(**row) for row in query_results.rows]

    def get_ancestors(self, subject_id: str) -> list[SubjectInfo]:
        query_results = self._qs.execute_named_query(
            "get_ancestors", subject_id=subject_id
        )
        return [
            SubjectInfo(
                id=make_id(data), name=data["name"], record_type=data["record_type"]
            )
            for data in query_results.rows
        ]

    def get_descendants(self, subject_id: str) -> list[SubjectInfo]:
        query_results = self._qs.execute_named_query(
            "get_descendants", subject_id=subject_id
        )
        return [
            SubjectInfo(
                id=make_id(data), name=data["name"], record_type=data["record_type"]
            )
            for data in query_results.rows
        ]

    def get_facets(self) -> list[SubjectInfo]:
        query_results = self._qs.execute_named_query("get_facets")
        return [
            SubjectInfo(
                id=make_id(data), name=data["name"], record_type=data["record_type"]
            )
            for data in query_results.rows
        ]

    def search(self, term):
        if len(term) < 3:
            return []
        cleaned_term = search_utils.clean_search_terms(term)
        query_results = self._qs.execute_named_query("search", term=cleaned_term)
        return [
            SubjectInfo(
                id=make_id(data), name=data["name"], record_type=data["record_type"]
            )
            for data in query_results.rows
        ]
