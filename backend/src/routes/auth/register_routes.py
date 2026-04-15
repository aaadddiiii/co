from flask import request
from werkzeug.security import generate_password_hash
from src.db.model import db, User, Teacher, Student
from src.utils import can_create_user, role_required, success, error, require_fields, validate_email, validate_positive, validate_int




def routes(app):

    # -------- REGISTER USER --------
    @app.route("/register", methods=["POST"])
    @can_create_user
    def register():

        data = request.form



        # -------- VALIDATION --------
        err = require_fields(data, ["name", "email", "password", "role"])
        if err:
            return error(err)

        name = data["name"].strip()
        email = data["email"].strip()
        password = data["password"]
        role = data["role"]

        if not validate_email(email):
            return error("Invalid email")

        if User.query.filter_by(email=email).first():
            return error("Email already exists")



        # -------- CREATE USER --------
        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            role=role
        )

        db.session.add(user)
        db.session.flush()  # get user.id without commit



        # -------- TEACHER --------
        if role == "teacher":
            type_, err = get_str(data, "type")
            if err: return err

            pay_rate, err = get_float(data, "pay_rate")
            if err: return err

            teacher = Teacher(
                user_id=user.id,
                type=type_,
                pay_rate=pay_rate
            )
            db.session.add(teacher)



        # -------- STUDENT --------
        elif role == "student":
            parent_id = data.get("parent_id")
            class_id = data.get("class_id", 1)

            if parent_id and not validate_int(parent_id):
                return error("Invalid parent_id")

            if not validate_int(class_id):
                return error("Invalid class_id")

            student = Student(
                user_id=user.id,
                parent_id=int(parent_id) if parent_id else None,
                class_id=int(class_id)
            )
            db.session.add(student)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return error("Database error", 500)

        return success(message="User created")

