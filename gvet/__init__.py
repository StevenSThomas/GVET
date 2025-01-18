import os

from flask import Flask, redirect, render_template, url_for
from flask_cors import CORS
from flask_login import login_required


def create_default_user():
    from .models import User

    default_user = User.query.filter_by(username="getty").first()
    if not default_user:
        User.create("getty", "getty", "JP Getty")


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
        create_default_user()

    # register blueprints
    from .auth import auth
    from .rest_api import rest_api

    app.register_blueprint(auth)
    app.register_blueprint(rest_api)

    @app.route(
        "/",
    )
    @login_required
    def index():
        return redirect("/gvet/")

    @app.route("/gvet/", defaults={"path": ""})
    @app.route("/gvet/<path:path>")
    @login_required
    def gvet(path):
        return render_template(
            "index.html",
            rest_api_base=url_for("rest_api.index"),
        )

    return app
