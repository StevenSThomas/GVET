import os
from flask import Flask, render_template, send_from_directory
from flask_cors import CORS

from flask_login import login_required, current_user
from gvet.gvp.services import QueryService


def create_app(test_config=None) -> Flask:
    """
    Initialize the web application
    """
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, origins=["http://localhost:*"])
    app.config.from_mapping(
        SECRET_KEY="DEV", SQLALCHEMY_DATABASE_URI="sqlite:///gvet.sqlite"
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    # setup database
    from .models import db

    db.init_app(app)
    with app.app_context():
        db.create_all()

    # register blueprints
    from .auth import auth
    from .api import api

    app.register_blueprint(auth)
    app.register_blueprint(api)

    @app.route("/")
    @login_required
    def index():
        return render_template("index.html")

    @app.route("/facets")
    @login_required
    def facets():
        qs = QueryService()
        facets = qs.get_facets()
        return render_template("subjects.html", subjects=facets)

    return app
