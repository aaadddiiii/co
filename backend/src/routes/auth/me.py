from flask import session
from src.db.model import User
from src.utils import success, error


def routes(app):

    @app.route("/me")
    def me():
        user_id = session.get("user_id")

        if not user_id:
            return error("Unauthorized", 401)

        user = User.query.get(user_id)

        if not user:
            return error("User not found", 404)

        return success(data={
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        })