from flask import request
from src.db.model import db, User, Teacher, Class
from src.utils import role_required, success, error, get_int, get_str


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


    
    @app.route("/teachers")
    @role_required("admin")
    def get_teachers():
        teachers = Teacher.query.all()

        return success(data=[
            {
                "id": t.id,
                "name": t.user.name
            } for t in teachers
        ])




    @app.route("/classes")
    @role_required("admin")
    def get_classes():
        classes = Class.query.all()

        return success(data=[
            {"id": c.id, "name": c.name}
            for c in classes
        ])



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





    @app.route("/users/<int:user_id>")
    @role_required("admin")
    def get_user_detail(user_id):
        user = User.query.get(user_id)

        if not user:
            return error("User not found", 404)

        data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }

        # teacher details
        if user.role == "teacher" and user.teacher:
            data["teacher"] = {
                "id": user.teacher.id,
                "type": user.teacher.type,
                "pay_rate": user.teacher.pay_rate
            }

        # student details
        if user.role == "student" and user.student_profile:
            data["student"] = {
                "id": user.student_profile.id,
                "class_id": user.student_profile.class_id,
                "parent_id": user.student_profile.parent_id,
                "status": user.student_profile.status
            }

        # parent details
        if user.role == "parent":
            data["children"] = [
                {
                    "id": s.id,
                    "class_id": s.class_id
                } for s in user.children
            ]

        return success(data=data)