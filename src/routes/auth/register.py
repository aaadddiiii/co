from flask import request, session
from werkzeug.security import generate_password_hash
from src.db.model import db, User, Teacher, Student
from src.utils import can_create_user


def is_allowed_to_create(user_id):
    user = User.query.get(user_id)

    if user.role == "admin":
        return True

    if user.role == "teacher":
        teacher = Teacher.query.filter_by(user_id=user.id).first()
        return teacher and teacher.type == "permanent"

    return False


def route(app):

    @app.route("/register", methods=["POST"])
    @can_create_user
    def register():

        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        role = request.form["role"]

        user = User(name=name, email=email, password=password, role=role)
        db.session.add(user)
        db.session.commit()

        # -------- TEACHER --------
        if role == "teacher":
            teacher = Teacher(
                user_id=user.id,
                type=request.form.get("type"),
                pay_rate=float(request.form.get("pay_rate", 0))
            )
            db.session.add(teacher)

        # -------- STUDENT --------
        elif role == "student":
            parent_id = request.form.get("parent_id")
            parent_id = int(parent_id) if parent_id else None

            class_id = int(request.form.get("class_id", 1))

            student = Student(
                user_id=user.id,
                parent_id=parent_id,
                class_id=class_id
            )
            db.session.add(student)

        db.session.commit()

        return "User created"