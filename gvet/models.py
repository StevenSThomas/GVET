from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class AuthenticationError(Exception):
    pass


class UserDoesNotExist(AuthenticationError):
    pass


class InvalidPassword(AuthenticationError):
    pass


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    display_name = db.Column(db.String(100))

    @classmethod
    def create(cls, username: str, password: str, display_name: str) -> "User":
        """Create a new user

                Encrypts a the password for storage

                Raises:
                  AttributeError: if user already exists
        ß
        """
        user = User.query.filter_by(username=username).first()
        if user:
            raise AttributeError("Username already exists.")
        new_user = cls(
            username=username,
            password=generate_password_hash(password),
            display_name=display_name,
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def authenticate(username: str, password: str) -> "User":
        """Attempts to authenticate a user by username and password

        Returns:
            a valid user instance if the username and password are valid

        Raises:
            UserDoesNotExist - if a user with the specified username cannot be found
            InvalidPassword - if the password does not match for the given user

        """
        user = User.query.filter_by(username=username).first()
        if not user:
            raise UserDoesNotExist()

        if not check_password_hash(user.password, password):
            raise InvalidPassword

        return user
