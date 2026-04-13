from flask import request, session
from werkzeug.security import check_password_hash
from src.db.model import User


def route(app):
    @app.route("/login", methods=["POST"])
    def login():
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["role"] = user.role
            return "Logged in"

        return "Invalid credentials", 401