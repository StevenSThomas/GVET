from dataclasses import asdict

from flask import Blueprint, jsonify, request, url_for
from flask_login import login_required

from gvet.gv import vocabulary
from gvet.gv.api import SubjectInfo

rest_api = Blueprint("rest_api", __name__, url_prefix="/api")


@rest_api.route("/")
@login_required
def index():
    return "Backend REST API for GVET"


@rest_api.route("/subjects/<subject_id>/brief")
def get_subject_info(subject_id: str):
    subject_info = vocabulary.get_subject_info(subject_id)
    context = _build_subject_info_context(subject_info)
    return jsonify(context)


@rest_api.route("/subjects/<subject_id>")
def get_subject_detail(subject_id: str):
    subject = vocabulary.get_subject_detail(subject_id)
    context = asdict(subject)
    context["_links"] = {
        "preferred_descendants": _url("get_subject_descendants", subject_id=subject_id),
    }

    return jsonify(context)


@rest_api.route("/subjects/<subject_id>/terms")
def get_subject_terms(subject_id: str):
    terms = vocabulary.get_terms(subject_id)
    return jsonify(terms)


@rest_api.route("/subjects/<subject_id>/notes")
def get_subject_notes(subject_id: str):
    notes = vocabulary.get_notes(subject_id)
    return jsonify(notes)


@rest_api.route("/subjects/<subject_id>/ancestors")
def get_subject_ancestors(subject_id: str):
    ancestors = vocabulary.get_ancestors(subject_id)
    return jsonify(ancestors)


@rest_api.route("/subjects/<subject_id>/descendants")
def get_subject_descendants(subject_id: str):
    result = vocabulary.get_descendants(subject_id)
    context = [_build_subject_info_context(subject_info) for subject_info in result]
    return jsonify(context)


@rest_api.route("/facets/")
def get_facets():
    facets = vocabulary.get_facets()
    context = [_build_subject_info_context(facet) for facet in facets]
    return jsonify(context)


@rest_api.route("/subjects/search")
def search():
    q = request.args.get("q")
    if not q:
        return []
    result = vocabulary.search(term=q)
    context = [_build_subject_info_context(subject_info) for subject_info in result]
    return jsonify(context)


# -- helper functions --


def _url(view_name: str, **kwargs):
    """helper function to build urls using common arguments"""
    return url_for(f"rest_api.{view_name}", **kwargs, _external=True)


def _build_subject_info_context(subject_info: SubjectInfo) -> dict:
    context = asdict(subject_info)
    context["_links"] = {
        "detail": _url("get_subject_detail", subject_id=subject_info.id),
        "terms": _url("get_subject_terms", subject_id=subject_info.id),
        "notes": _url("get_subject_notes", subject_id=subject_info.id),
        "preferred_descendants": _url(
            "get_subject_descendants", subject_id=subject_info.id
        ),
    }
    return context
