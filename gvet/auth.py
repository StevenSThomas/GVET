from flask import Blueprint, request, flash, redirect, url_for, render_template
from gvet.models import User, AuthenticationError
from flask_login import login_user, login_required, logout_user, LoginManager

# Setup the 'auth' blueprint
_login_manager = LoginManager()
_login_manager.login_view = "auth.login"
_login_manager.login_message = None


@_login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class _AuthBlueprint(Blueprint):
    def register(self, app, options):
        _login_manager.init_app(app)
        return super().register(app, options)


auth = _AuthBlueprint("auth", __name__)


@auth.get("/login")
def login():
    return render_template("auth/login.html")


@auth.post("/login")
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")

    try:
        user = User.authenticate(username, password)
    except AuthenticationError:
        flash("Incorrect username or password. Please try again.")
        return redirect(url_for("auth.login"))
    login_user(user, remember=True)
    return redirect(url_for("index"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
