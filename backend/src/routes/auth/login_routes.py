from flask import request, session
from src.utils import success, error, require_fields
from src.db.model import User
from werkzeug.security import check_password_hash


def routes(app):
    @app.route("/login", methods=["POST"])
    def login():
        data = request.form

        err = require_fields(data, ["email", "password"])
        if err:
            return error(err)

        user = User.query.filter_by(email=data["email"]).first()

        if not user or not check_password_hash(user.password, data["password"]):
            return error("Invalid credentials", 401)

        session["user_id"] = user.id
        session["role"] = user.role

        return success(message="Logged in")