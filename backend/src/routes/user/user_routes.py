from flask import request
from src.db.model import db, User
from src.utils import role_required
from src.utils.response import success, error
from src.utils.request_utils import get_int, get_str


def routes(app):

    # -------- GET ALL USERS --------
    @app.route("/users", methods=["GET"])
    @role_required("admin")
    def get_users():
        users = User.query.all()

        data = [
            {
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "role": u.role
            } for u in users
        ]

        return success(data=data)

    # -------- UPDATE USER --------
    @app.route("/users/update", methods=["POST"])
    @role_required("admin")
    def update_user():
        data = request.form

        user_id, err = get_int(data, "id")
        if err: return err

        user = User.query.get(user_id)
        if not user:
            return error("User not found", 404)

        name = data.get("name")
        email = data.get("email")
        role = data.get("role")

        if name:
            user.name = name.strip()

        if email:
            user.email = email.strip()

        if role:
            user.role = role

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return error("Database error", 500)

        return success(message="User updated")

    # -------- DELETE USER --------
    @app.route("/users/delete", methods=["POST"])
    @role_required("admin")
    def delete_user():
        data = request.form

        user_id, err = get_int(data, "id")
        if err: return err

        user = User.query.get(user_id)
        if not user:
            return error("User not found", 404)

        if user.id == session.get("user_id"):
            return error("Cannot delete yourself")

        if user.role == "admin":
            return error("Cannot delete admin")

        try:
            db.session.delete(user)
            db.session.commit()
        except:
            db.session.rollback()
            return error("Database error", 500)

        return success(message="User deleted")