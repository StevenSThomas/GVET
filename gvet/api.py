from flask import Blueprint
from flask_login import login_required
from gvet import gvp
from dataclasses import asdict

api = Blueprint("api", __name__, url_prefix="/api")

gvp_service = gvp.QueryService()


@api.route("/")
@login_required
def index():
    return "it worked!"


@api.route("/facets")
def get_facets():
    facets = gvp_service.get_facets()
    return [asdict(facet) for facet in facets]
